import pandas as pd


from dataframe_to_superset import SupersetAccessor

SupersetAccessor.configure(
    base_url="http://dw.schuurman.intra",
    username="test_ldap",
    password="Schuur310!",
    provider="ldap",  # or "db"
    database_name="superset_temp_ludo",
    schema="public",  # optional, defaults to "public"
)
data = {"name": ["Alice", "Bob"], "age": [25, 30]}
df = pd.DataFrame(data)


url = df.superset.to_superset("example_dataset")
print(url)
