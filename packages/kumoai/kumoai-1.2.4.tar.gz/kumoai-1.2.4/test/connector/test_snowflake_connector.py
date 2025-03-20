import pandas as pd
import pytest
import requests_mock
from kumoapi.data_source import DataSourceType
from kumoapi.json_serde import to_json_dict
from kumoapi.source_table import (
    SourceTableDataResponse,
    SourceTableListResponse,
)
from kumoapi.typing import Dtype

from kumoai import global_state
from kumoai.connector import SnowflakeConnector
from kumoai.connector.source_table import SourceTable
from kumoai.exceptions import HTTPException
from kumoai.testing import onlyIntegrationTest


@pytest.fixture(scope="class")
def mock_connector(setup_mock_client,
                   mock_api: requests_mock.Mocker) -> SnowflakeConnector:
    # Mock the connector creation API to return 200:
    mock_api.get(f'{global_state.client._api_url}/connectors/snowflake',
                 status_code=404)
    mock_api.post(f"{global_state.client._api_url}/connectors")
    return SnowflakeConnector(
        'snowflake', 'acc', 'warehouse', 'db', 'schema', credentials={
            'user': 'fake_user',
            'password': 'fake_password'
        })


class TestMockSnowflakeConnectorLifecycle:
    r"""Groups mock tests that pertain to the Snowflake connector
    lifecycle. Note that these tests are expected to run sequentially.
    """
    def test_properties(self, mock_connector: SnowflakeConnector):
        assert str(mock_connector) == (
            'SnowflakeConnector(account="acc", database="DB", schema="SCHEMA")'
        )
        assert mock_connector.name == "snowflake"
        assert mock_connector.source_type == DataSourceType.SNOWFLAKE

    def test_table_names(self, mock_connector: SnowflakeConnector,
                         mock_api: requests_mock.Mocker):
        # NOT OK: mock list_tables endpoint returning error:
        mock_api.post(
            f"{global_state.client._api_url}/source_tables/list_tables",
            [{
                'text': 'Failed request!',
                'status_code': 500
            }],
        )
        with pytest.raises(HTTPException, match="Failed request!"):
            mock_connector.table_names()

        res = SourceTableListResponse(table_names=['table_1', 'table_2'])

        # 200 OK: mock list_tables endpoint returning two source tables:
        mock_api.post(
            f"{global_state.client._api_url}/source_tables/list_tables",
            [{
                'json': to_json_dict(res),
                'status_code': 200
            }])
        assert set(mock_connector.table_names()) == {'table_1', 'table_2'}

    def test_get_table(self, mock_connector: SnowflakeConnector,
                       mock_api: requests_mock.Mocker):
        # NOT OK: mock list_tables endpoint returning error:
        mock_api.post(
            f"{global_state.client._api_url}/source_tables/list_tables",
            [{
                'text': 'Failed request!',
                'status_code': 500
            }],
        )
        with pytest.raises(ValueError, match="does not exist"):
            mock_connector.table('table_1')
        with pytest.raises(ValueError, match="does not exist"):
            mock_connector['table_1']
        assert 'table_1' not in mock_connector

        # 200 OK: mock list_tables endpoint returning OK for the input table
        res = SourceTableListResponse(table_names=['table_1'])
        mock_api.post(
            f"{global_state.client._api_url}/source_tables/list_tables",
            [{
                'json': to_json_dict(res),
                'status_code': 200
            }])
        assert 'table_1' in mock_connector
        assert 'table_2' not in mock_connector
        assert isinstance(mock_connector.table('table_1'), SourceTable)
        assert isinstance(mock_connector['table_1'], SourceTable)

    def test_table_head(self, mock_connector: SnowflakeConnector,
                        mock_api: requests_mock.Mocker):
        test_dataframe = pd.DataFrame({
            "one":
            pd.Series([1.0, 2.0, 3.0], index=["a", "b", "c"]),
            "two":
            pd.Series([1.0, 2.0, 3.0, 4.0], index=["a", "b", "c", "d"]),
        })

        res = SourceTableDataResponse(
            table_name='table_1',
            cols=[],
            sample_rows=test_dataframe.to_json(orient='table'),
        )

        # NOT OK: mock list_tables endpoint returning error:
        mock_api.post(
            f"{global_state.client._api_url}/source_tables/list_tables",
            [{
                'json': to_json_dict(SourceTableListResponse(table_names=[])),
                'status_code': 200
            }])
        mock_api.post(
            f"{global_state.client._api_url}/source_tables/get_table_data",
            [{
                'text': 'Failed request!',
                'status_code': 500
            }],
        )
        with pytest.raises(ValueError, match="does not exist"):
            mock_connector.table('table_1').head()

        # 200 OK: mock list_tables endpoint returning a valid dataframe
        # response when fetching sample rows:
        mock_api.post(
            f"{global_state.client._api_url}/source_tables/list_tables", [{
                'json':
                to_json_dict(SourceTableListResponse(table_names=['table_1'])),
                'status_code':
                200
            }])
        mock_api.post(
            f"{global_state.client._api_url}/source_tables/get_table_data",
            [{
                'json': [to_json_dict(res)],
                'status_code': 200
            }])

        table_head = mock_connector.table('table_1').head()
        assert isinstance(table_head, pd.DataFrame)

        # TODO(manan): float dtype mismatch!
        # pd.testing.assert_frame_equal(test_dataframe, table_head)


@pytest.fixture(scope="class")
def integ_connector(setup_integration_client):
    connector = SnowflakeConnector(
        'snowflake',
        account='xva19026',
        warehouse='WH_XS',
        database='KUMO',
        schema_name='FINANCIAL',
    )

    # Run the test:
    yield connector

    connector._delete_connector()


class TestSnowflakeConnectorLifecycle:
    r"""Groups integration tests that pertain to the Snowflake connector
    lifecycle. Note that these tests are expected to run sequentially.
    """
    @onlyIntegrationTest
    def test_properties(self, integ_connector: SnowflakeConnector):
        assert str(integ_connector) == (
            'SnowflakeConnector(account="xva19026", database="KUMO", '
            'schema="FINANCIAL")')

    @onlyIntegrationTest
    def test_table_names(self, integ_connector: SnowflakeConnector):
        r"""Test that table names load properly."""
        table_names = integ_connector.table_names()
        assert len(table_names) > 0
        assert 'TRANS' in table_names

    @onlyIntegrationTest
    def test_get_table(self, integ_connector: SnowflakeConnector):
        trans_table = integ_connector.table('TRANS')
        assert isinstance(trans_table, SourceTable)

        # Table metadata:
        assert {c.name
                for c in trans_table.columns} == set([
                    'TRANS_ID', 'ACCOUNT_ID', 'TYPE', 'OPERATION', 'AMOUNT',
                    'BALANCE', 'K_SYMBOL', 'BANK', 'ACCOUNT', 'DATE'
                ])
        assert trans_table.column_dict['TRANS_ID'].dtype == Dtype.int64

        # Table data:
        df = trans_table.head(num_rows=7)
        assert isinstance(df, pd.DataFrame)
        assert set([c.name for c in trans_table.columns]) == set(df.columns)
        assert len(df) == 7
