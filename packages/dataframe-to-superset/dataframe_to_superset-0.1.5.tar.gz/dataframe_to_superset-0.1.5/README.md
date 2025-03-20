# Superset Accessor for Pandas DataFrames

> **Note**: The code docs AI-generated so may not be perfect (or even right lol).

[![PyPI version](https://img.shields.io/pypi/v/dataframe-to-superset)](https://pypi.org/project/dataframe-to-superset/)

Upload your DataFrame to Superset as a datasource for rapid visualization.
## Notes

- Ensure you have a database or datasource in Superset that supports CSV uploads.
- Ensure API access is enabled.
- To maintain a clean and organized Superset environment:
    - Within Superset create a dedicated database or datasource (specified by the `database_name` parameter in the `configure` function) for this package.
    - Consistently use the same database or datasource name when uploading data, as the package overwrites existing data by default.
- Call `SupersetAccessor.configure` at least once before using the `as_datasource` accessor.

## Installation

Install the package via pip:

```sh
pip install dataframe-to-superset
```

## Usage
```python
import pandas as pd
from dataframe_to_superset import SupersetAccessor

SupersetAccessor.configure(
    base_url="https://superset",
    username="your_username",
    password="your_password",
    provider="your_auth_provider",  # e.g., "ldap" or "db"
    database_name="your_database_name",
    schema="your_schema_name",  # optional, defaults to "public"
)

data = {"name": ["Alice", "Bob"], "age": [25, 30]}
df = pd.DataFrame(data)

url = df.superset.as_datasource("people")
print(url)

# Another example
data = {"animal": ["Wolf", "Cat"], "Sound": ["Howl", "Meow"]}
df = pd.DataFrame(data)

url = df.superset.as_datasource("animal_sounds", verbose_return = True)
print(url)
```
### Configuration Parameters for `configure` Function

| Parameter       | Type                                   | Default       | Description                                                                 |
|-----------------|----------------------------------------|---------------|-----------------------------------------------------------------------------|
| `base_url`      | `str`                                 |               | URL of Superset instance. `/api/v1` is automatically appended.         |
| `username`      | `str`                                 |               |                                       |
| `password`      | `str`                                 |               |                            |
| `provider`      | `Literal["db", "ldap", "oauth", "oid", "remote_user"]` |               | Indicates the authentication provider type.                                 |
| `database_name` | `str`                                 |               | Name of the database/datasource in Superset where data will be uploaded.                 |
| `schema`        | `str`                                 | `"public"`    | Specifies the schema to upload data to (should exist on the database).                                     |

---

### Parameters for `as_datasource` Method

| Parameter        | Type        | Default                                      | Description                                                                 |
|------------------|-------------|----------------------------------------------|-----------------------------------------------------------------------------|
| `dataset_name`   | `str`       | `{username}_generated_dataset_{random_suffix}` | Name of the dataset in Superset. |
| `replace`        | `bool`      | `True`                                       | Replace the existing dataset based on the `dataset_name` (if it already exists).        |
| `verbose_return` | `bool`      | `False`                                      | Return detailed information in stead of only the url |

---
### Return Types for `as_datasource` Method

| Return Type                  | Description                                                                 | Example Response                                                                 |
|------------------------------|-----------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| `Dict[str, Any]` (if `verbose_return=True`) | Dictionary with detailed information about the created/updated dataset. | `{"dataset_id": 123, "name": "animal_sounds", "url": "https://superset/explore/?dataset_id=123"}` |
| `str` (if `verbose_return=False`)          | URL of the uploaded dataset for direct visualisation access`. | `"https://superset/explore/?dataset_id=123"`                                     |
