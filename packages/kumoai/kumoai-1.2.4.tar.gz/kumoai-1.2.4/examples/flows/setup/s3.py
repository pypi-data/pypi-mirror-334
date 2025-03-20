r"""Connecting data on Amazon S3.

This script covers all setup and initialization CUJs on the S3 object store.
CUJs that are not supported are explicitly marked below.
"""
import pandas as pd
from kumoapi.source_table import SourceColumn

import kumoai as kumo

API_URL = "http://localhost:10002"
API_KEY = "test:DISABLED"
kumo.init(url=API_URL, api_key=API_KEY)

path = "s3://kumo-public-datasets/customerltv_mini/"

# 1. You can create an S3 connector on a root directory by passing a path:
connector = kumo.S3Connector(path)

# 2. You can create an S3 connector without any root directory, and pass
# paths through the connector:
connector_global = kumo.S3Connector()

# 3. You CANNOT load an S3 connector by name (e.g. from the UI).

# 4. You can list all tables behind an S3 connector, if a path is specified:
# 4a) Returns tables behind a specified directory:
table_names = connector.table_names()
assert set(table_names) == {'customer', 'stock', 'transaction'}

# 4b) Raises an appropriate error:
try:
    table_names = connector_global.table_names()
except ValueError as e:
    assert "not supported" in str(e)
else:
    raise RuntimeError("Exception not raised.")

# 5. You can read the schema information from a raw table in a given connector:
# 5a) You can fetch column names and data types:
customer = connector['customer']
columns = customer.columns
assert columns == [
    SourceColumn(name='CustomerID', stype='numerical', dtype='float64',
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
