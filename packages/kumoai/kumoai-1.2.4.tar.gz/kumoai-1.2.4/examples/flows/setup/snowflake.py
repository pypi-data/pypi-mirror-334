r"""Connecting data on Snowflake. Please note that running this example script
requires setting either:
    * SNOWFLAKE_USER and SNOWFLAKE_PASSWORD or
    * SNOWFLAKE_PRIVATE_KEY
environment variables. This script can be slightly modified for SPCS native
apps, by passing the relevant credentials into `kumo.init`.

This script covers all setup and initialization CUJs on the Snowflake data
warehouse. CUJs that are not supported are explicitly marked below.
"""
import os

import pandas as pd
from kumoapi.source_table import SourceColumn

import kumoai as kumo

API_URL = "http://localhost:10002"
API_KEY = "test:DISABLED"
kumo.init(url=API_URL, api_key=API_KEY)

# 1. You can connect to all supported connections Snowflake without plaintext
# passwords and additional setup:
# 1a) Configure secure connections using environment variables or encrypted
# credentials (these are provided based on the environment variables above):
connector = kumo.SnowflakeConnector(
    name="snowflake_connector",
    account="xva19026",
    warehouse="WH_XS",
    database="KUMO",
    schema_name="CUSTOMER_LTV",
)

# 1b) Connection errors are clearly logged with troubleshooting gudiance:
if "SNOWFLAKE_USER" in os.environ:
    del os.environ["SNOWFLAKE_USER"]
if "SNOWFLAKE_PRIVATE_KEY" in os.environ:
    del os.environ["SNOWFLAKE_PRIVATE_KEY"]

try:
    _ = kumo.SnowflakeConnector(
        name="snowflake_connector",
        account="xva19026",
        warehouse="WH_XS",
        database="KUMO",
        schema_name="CUSTOMER_LTV",
    )
except ValueError as e:
    assert "Please pass a" in str(e)
else:
    raise RuntimeError("Exception not raised.")

# 3. You can load a Snowflake connector by name (e.g. from the UI).
# 3a) Use name (created above):
connector = kumo.SnowflakeConnector.get_by_name("snowflake_connector")

# 3b) Invalid names raise appropriate errors:
try:
    _ = kumo.SnowflakeConnector.get_by_name("invalid_name")
except ValueError as e:
    assert "does not exist" in str(e)
else:
    raise RuntimeError("Exception not raised.")

# 4. You can list all tables behind a Snowflake connector:
table_names = connector.table_names()
assert {'customer', 'stock', 'transaction'}.issubset(set(table_names))

# 5. You can read the schema information from a raw table in a given connector:
# 5a) You can fetch column names and data types:
customer = connector['customer']
columns = customer.columns
assert columns == [
    SourceColumn(name='CustomerID', stype='numerical', dtype='float',
                 is_primary=False)
]
# 5b) Error handling if table name is wrong:
try:
    nonexistent = connector['nonexistent']
except ValueError as e:
    assert "does not exist" in str(e)
else:
    raise RuntimeError("Exception not raised.")

# 6. Read a limited # of samples from a raw table in a given connector:
customer = connector['customer']
head_rows = customer.head(num_rows=10)
assert isinstance(head_rows, pd.DataFrame)
assert len(head_rows) == 10
