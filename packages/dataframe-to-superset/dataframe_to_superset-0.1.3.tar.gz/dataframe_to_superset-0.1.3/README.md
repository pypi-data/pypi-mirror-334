# Superset Accessor for Pandas DataFrames

> **Note**: The code docs AI-generated so may not be perfect (or even right lol).

[![PyPI version](https://badge.fury.io/py/dataframe-to-superset.svg)](https://pypi.org/project/dataframe-to-superset/)
[![GitHub](https://img.shields.io/github/issues/lodu/dataframe-to-superset.svg?style=social&label=Issues)](https://github.com/lodu/dataframe-to-superset)

Upload your DataFrame to Superset as a datasource for rapid visualization.
## Notes

- Ensure you have a database or datasource in Superset that supports CSV uploads.
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
