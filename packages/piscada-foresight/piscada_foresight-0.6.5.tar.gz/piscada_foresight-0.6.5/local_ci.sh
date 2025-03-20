#!/bin/bash

# Script: bitbucket-pipeline-runner.sh
# Description: Runs specified steps from a bitbucket-pipelines.yml file locally
# Requirements: docker, yq
# Usage: ./bitbucket-pipeline-runner.sh [-f pipeline_file] [-s steps]

set -euo pipefail

# Default values
PIPELINE_FILE="bitbucket-pipelines.yml"
STEPS="Test,Lint"

# Function to display usage information
show_usage() {
    echo "Usage: $0 [-f pipeline_file] [-s steps]"
    echo "  -f: Path to bitbucket-pipelines.yml file (default: ./bitbucket-pipelines.yml)"
    echo "  -s: Comma-separated list of steps to run (default: test,lint)"
    exit 1
}

# Function to log messages
log() {
    local level="$1"
    shift
    echo "[${level}] $*"
}

# Function to check dependencies
check_dependencies() {
    local missing_deps=0

    if ! command -v docker >/dev/null 2>&1; then
        log "ERROR" "Docker is not installed"
        missing_deps=1
    fi

    if ! command -v yq >/dev/null 2>&1; then
        log "ERROR" "yq is not installed"
        missing_deps=1
    fi

    if [ $missing_deps -eq 1 ]; then
        exit 1
    fi
}

# Function to run a single step
run_step() {
    local step_name="$1"
    local image
    local script_commands
    local default_image="atlassian/default-image:latest"

    # Check if the step exists in the pipeline file
    # yq will return null/empty if no matching step found
    STEP_EXISTS=$(yq eval ".definitions.steps[] | select(has(\"step\")) | select(.step.name == \"${step_name}\") | .step.name" "${PIPELINE_FILE}")
    if [[ -z "${STEP_EXISTS}" ]]; then
        log "ERROR" "Step ${step_name} not found in pipeline file"
        return 1
    fi

    # Extract step information using yq by getting the actual step definition
    image=$(yq eval ".definitions.steps[] | select(has(\"step\")) | select(.step.name == \"${step_name}\") | .step.image" "${PIPELINE_FILE}")

    if [ -z "${image}" ]; then
        image="${default_image}"
    fi

    log "INFO" "Running step: ${step_name}"
    log "INFO" "Pulling image: ${image}"

    # Pull the Docker image
    docker pull "${image}" >/dev/null

    # Create temporary script file
    local temp_script
    temp_script=$(mktemp)
    script_commands=$(yq eval ".definitions.steps[] | select(has(\"step\")) | select(.step.name == \"${step_name}\") | .step.script[]" "${PIPELINE_FILE}")
    echo "${script_commands}" > "${temp_script}"

    # Run the commands in Docker
    log "INFO" "Executing ${step_name} commands..."
    docker run --rm \
        -e UV_CACHE_DIR="/tmp/.uv-cache" \
        -v "$(pwd):/workspace" \
        -w "/workspace" \
        -u "$(id -u):$(id -g)" \
        "${image}" \
        /bin/bash -c "$(cat "${temp_script}")"

    local exit_code=$?
    rm "${temp_script}"

    if [ $exit_code -eq 0 ]; then
        log "INFO" "Step ${step_name} completed successfully"
    else
        log "ERROR" "Step ${step_name} failed with exit code ${exit_code}"
        return 1
    fi
}

# Parse command line arguments
while getopts ":f:s:h" opt; do
    case ${opt} in
        f )
            PIPELINE_FILE=$OPTARG
            ;;
        s )
            STEPS=$OPTARG
            ;;
        h )
            show_usage
            ;;
        \? )
            echo "Invalid option: -$OPTARG" 1>&2
            show_usage
            ;;
        : )
            echo "Option -$OPTARG requires an argument" 1>&2
            show_usage
            ;;
    esac
done

# Main execution
main() {
    # Check if pipeline file exists
    if [ ! -f "${PIPELINE_FILE}" ]; then
        log "ERROR" "Pipeline file ${PIPELINE_FILE} not found"
        exit 1
    fi

    # Check dependencies
    check_dependencies

    # Convert comma-separated steps to array
    IFS=',' read -ra STEP_ARRAY <<< "${STEPS}"

    # Run each specified step
    for step in "${STEP_ARRAY[@]}"; do
        if ! run_step "${step}"; then
            log "ERROR" "Failed to run step: ${step}"
            exit 1
        fi
    done

    log "INFO" "All steps completed successfully"
}

main
