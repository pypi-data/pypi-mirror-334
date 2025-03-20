# Test Summary

Below is an organized summary of all the test functions found in your code, grouped by feature area and functionality.

---

## 1. `get_values` Tests

### 1.1 Raw Timeseries

| **Test Name**                           | **Description**                                                                                                               | **Expected Outcome**                                                                                                                                               |
|-----------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `test_get_values_success`               | Ensures the function returns a valid `DataFrame` from raw timeseries data and gracefully handles missing first values as `NaN`. | - Verifies the returned `DataFrame` length.<br/>- Checks that the first row in a specific column is `NaN`.                                                        |
| `test_get_values_missing_values`        | Tests the scenario where no values are found in the specified time range.                                                    | - Raises a `RuntimeError` if no data is found.                                                                                                                    |
| `test_get_values_start_later_than_end`  | Verifies that the function raises a `ValueError` when the `start` datetime is after the `end` datetime.                     | - Raises a `ValueError` indicating an invalid time range (`start > end`).                                                                                         |
| `test_get_values_start_or_end_not_timezone_aware` | Checks that naive (not timezone-aware) datetimes for `start` or `end` are rejected.                                       | - Raises a `ValueError` if the parameters lack timezone information.                                                                                              |

### 1.2 Aggregated Timeseries

| **Test Name**                                                            | **Description**                                                                                                   | **Expected Outcome**                                                                                                                                                     |
|--------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `test_get_values_aggregated_success`                                     | Tests retrieval and parsing of aggregated data with valid aggregation functions (e.g., `min`, `max`, `avg`).      | - Returns a non-empty `DataFrame` with columns for each aggregator.<br/>- Validates expected columns like `(...|min)`, `(...|max)`, `(...|avg)`, `(...|count)`, `(...|last)`. |
| `test_get_values_aggregated_missing_values`                              | Checks behavior for aggregated timeseries with no data.                                                          | - Raises a `RuntimeError` if the response contains no aggregated data.                                                                                                                                          |
| `test_get_values_aggregated_invalid_aggregator`                          | Verifies that an invalid aggregator name (e.g., `foo`) raises a `ValueError`.                                    | - Expects a `ValueError` mentioning "Invalid aggregation function provided".                                                                                                                                     |
| `test_get_values_aggregated_multiple_aggregators`                        | Ensures multiple valid aggregations (e.g., `min`, `max`, `avg`) can be combined successfully.                    | - Returns a `DataFrame` with columns for each aggregator and each entity.                                                                                                                                        |
| `test_get_values_aggregated_interval_none_uses_default`                  | Checks that `interval=None` defaults to a specific interval (e.g., `1d`).                                        | - Verifies that the query is made with `interval='1d'`.<br/>- Confirms the returned `DataFrame` is valid.                                                                                                       |
| `test_get_values_aggregated_end_none_uses_now`                           | Checks that if `end=None`, it defaults to `datetime.now(timezone.utc)`.                                          | - Returns a non-empty `DataFrame`, confirming data retrieval was successful.                                                                                                                                    |
| `test_get_values_aggregated_start_later_than_end_raises_error`           | Verifies an exception is raised when `start` is after `end` in an aggregated query.                               | - Raises a `ValueError` indicating "The 'start' datetime cannot be later than the 'end' datetime.".                                                                                                              |
| `test_get_values_aggregated_start_or_end_not_timezone_aware_raises_error`| Ensures that naive datetimes (`start` or `end`) are rejected for aggregated queries.                              | - Expects a `ValueError` if `start` or `end` lacks timezone info.                                                                                                                                               |

---

## 2. Domain (Brick) Tests

These tests focus on retrieving and manipulating domain-related data (e.g., Brick definitions, traits, relationships).

| **Test Name**                          | **Description**                                                                                                          | **Expected Outcome**                                                                                                                                                                                                |
|---------------------------------------|--------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `test_get_domains`                    | Tests retrieving domain information and verifying domain/trait objects.                                                 | - Expects the correct number of domains (e.g., `16`).<br/>- Confirms domain attributes (`prefix`, `uri`).<br/>- Validates trait attributes (`id`, `parent_ids`, `child_ids`, etc.).                                                                         |
| `test_get_trait_by_id`                | Tests retrieving a single trait by its ID.                                                                              | - Retrieves and checks the correct trait (e.g., `brick:Building`) with expected properties.                                                                                                                          |
| `test_get_parent_traits`              | Tests retrieving all parent traits of a given trait.                                                                    | - Ensures all ancestor traits (e.g., `brick:Point`, `brick:Sensor`) are included in the result.                                                                                                                      |
| `test_get_trait_by_id_exceptions`     | Tests error handling for trait lookups (e.g., non-existent IDs, empty trait lists).                                     | - Raises `KeyError` if the trait does not exist.<br/>- Raises an exception if the domain has no traits.                                                                                                              |
| `test_get_parent_traits_exceptions`   | Covers special cases when retrieving parent traits (e.g., missing parent IDs, cyclic references).                       | - Raises `RecursionError` if a cyclic parent reference is detected.<br/>- Returns the trait itself if no parents exist or if `parent_ids` is `None`.                                                                 |
| `test_get_trait_by_id_with_domains`   | Tests retrieving a trait by ID across multiple domains.                                                                 | - Returns the trait if found; otherwise raises `ValueError`.<br/>- Raises `ValueError` for an empty domain list.<br/>- May raise `TypeError` or `AttributeError` if the domain data is invalid.                      |

---

## 3. `http_piscada` Tests

| **Test Name**         | **Description**                                                                                           | **Expected Outcome**                                                                                                    |
|-----------------------|-----------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|
| `test_get_state_file` | Tests generation of a path to a state file for a given name within the `http_piscada` module's local dir. | - Expects a path ending with `/.test_state` and starting with `/`, confirming correct location and naming convention.    |

---

### Additional Notes
- All tests use the **pytest** framework.
- Assertions are used to confirm expected outcomes, and any expected errors are handled using `pytest.raises(...)`.
- This structure helps quickly identify the purpose and outcome of each test, making it easier to maintain and extend in the future.
