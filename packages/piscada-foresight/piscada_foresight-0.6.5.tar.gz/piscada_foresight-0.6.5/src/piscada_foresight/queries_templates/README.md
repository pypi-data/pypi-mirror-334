# GraphQL Query Templates

This directory contains GraphQL query templates using Jinja2 for dynamic query generation and static queries for predefined GraphQL requests.

## Naming Convention

- **Dynamic Queries**: `<query_name>.j2`  
  Templates with placeholders that can be rendered dynamically with variables.
  
- **Static Queries**: `<query_name>.graphql`  
  Predefined static GraphQL queries without dynamic placeholders.

## Available Queries

### TimeSeries

- **`aggregated_timeseries.j2`**  
  Fetches aggregated timeseries data for multiple entities.

- **`raw_timeseries.j2`**  
  Fetches raw timeseries data for multiple entities.

### Domains

- **`get_domains.graphql`**  
  Fetches domain definitions, including their names, prefixes, descriptions, URIs, and detailed hierarchical relationships for traits and relationships within each domain.

## Usage

To load and render queries, use the `load_query` function defined in `query_loader.py`. This function supports dynamic rendering of queries by passing variables to the Jinja2 templates.

### Example Usage

```python
from query_loader import load_query

# Example: Load a dynamic query
query = load_query('aggregated_timeseries.j2', start_time='2023-01-01T00:00:00Z', end_time='2023-01-31T23:59:59Z')
print(query)

# Example: Load a static query
query = load_query('get_domains.graphql')
print(query)
