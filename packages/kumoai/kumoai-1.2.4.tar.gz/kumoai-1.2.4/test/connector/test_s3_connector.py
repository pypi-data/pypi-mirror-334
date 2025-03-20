import pandas as pd
import pytest
import requests_mock
from kumoapi.data_source import DataSourceType
from kumoapi.json_serde import to_json_dict
from kumoapi.source_table import (
    SourceTableDataResponse,
    SourceTableListResponse,
)

from kumoai import global_state
from kumoai.connector import S3Connector, SourceTable
from kumoai.testing import onlyIntegrationTest


@pytest.fixture(scope="class")
def connector(setup_mock_client) -> S3Connector:
    # NOTE: right now, the S3 connector does not actually perform any creation
    # logic in the backend, so this is a no-op. If this changes in the future,
    # the fixture needs updating:
    return S3Connector()


class TestMockS3ConnectorLifecycle:
    r"""Groups mock tests that pertain to the S3 connector
    lifecycle. Note that these tests are expected to run sequentially.
    """
    def test_properties(self, connector: S3Connector):
        assert str(connector) == "S3Connector(root_dir=None)"
        assert connector.name == "s3_connector"
        assert connector.source_type == DataSourceType.S3

    def test_table_names(self, connector: S3Connector):
        # TODO(manan): implement
        pass

    def test_get_table_when_list_tables_fail(
        self,
        connector: S3Connector,
        mock_api: requests_mock.Mocker,
    ):
        path = "s3://bucket/table"

        # NOT OK: mock list_tables endpoint returning error:
        mock_api.post(
            f"{global_state.client._api_url}/source_tables/list_tables",
            [{
                'text': 'Failed request!',
                'status_code': 500
            }],
        )
        with pytest.raises(ValueError, match="does not exist"):
            connector.table(path)

    def test_get_table_when_tables_found(
        self,
        connector: S3Connector,
        mock_api: requests_mock.Mocker,
    ):
        path = "s3://bucket/table"
        res = SourceTableListResponse(table_names=[path])

        # 200 OK: mock list_tables endpoint returning OK for the input table
        mock_api.post(
            f"{global_state.client._api_url}/source_tables/list_tables",
            [{
                'json': to_json_dict(res),
                'status_code': 200
            }])

        assert path in connector
        assert isinstance(connector.table(path), SourceTable)
        assert isinstance(connector[path], SourceTable)

    def test_get_table_when_tables_with_trailing_slashes(
        self,
        connector: S3Connector,
        mock_api: requests_mock.Mocker,
    ):
        path = "s3://bucket/table"
        res = SourceTableListResponse(table_names=[path])

        # 200 OK: mock list_tables endpoint returning OK for the input table
        mock_api.post(
            f"{global_state.client._api_url}/source_tables/list_tables",
            [{
                'json': to_json_dict(res),
                'status_code': 200
            }])

        # Validating that contains can handle trailing //
        assert f'{path}//' in connector
        assert isinstance(connector.table(path), SourceTable)
        assert isinstance(connector[path], SourceTable)

    def test_table_head(self, connector: S3Connector,
                        mock_api: requests_mock.Mocker):
        test_dataframe = pd.DataFrame({
            "one":
            pd.Series([1.0, 2.0, 3.0], index=["a", "b", "c"]),
            "two":
            pd.Series([1.0, 2.0, 3.0, 4.0], index=["a", "b", "c", "d"]),
        })

        test_path = 's3://bucket/path'
        res = SourceTableDataResponse(
            table_name='path',
            cols=[],
            sample_rows=test_dataframe.to_json(orient='table'),
        )

        # NOT OK: mock list_tables endpoint returning error:
        mock_api.post(
            f"{global_state.client._api_url}/source_tables/list_tables",
            [{
                'json': to_json_dict(
                    SourceTableListResponse(table_names=[''])),
                'status_code': 200
            }])
        mock_api.post(
            f"{global_state.client._api_url}/source_tables/get_data",
            [{
                'text': 'Failed request!',
                'status_code': 500
            }],
        )
        with pytest.raises(ValueError, match="does not exist"):
            connector.table(test_path).head()

        # 200 OK: mock get_table_data endpoint returning a valid dataframe
        # response when fetching sample rows:
        mock_api.post(
            f"{global_state.client._api_url}/source_tables/list_tables", [{
                'json':
                to_json_dict(SourceTableListResponse(table_names=[test_path])),
                'status_code':
                200
            }])
        mock_api.post(
            f"{global_state.client._api_url}/source_tables/get_table_data",
            [{
                'json': [to_json_dict(res)],
                'status_code': 200
            }])

        table_head = connector.table(test_path).head()
        assert isinstance(table_head, pd.DataFrame)


@pytest.fixture(scope="class")
def integ_connector(setup_integration_client):
    yield S3Connector()


class TestSnowflakeConnectorLifecycle:
    r"""Groups integration tests that pertain to the Snowflake connector
    lifecycle. Note that these tests are expected to run sequentially.
    """

    # TODO(manan): test on financial, like Snowflake...
    base_path = ("s3://kumo-public-datasets/Kumo-Experience-Bug-Bash-Datasets/"
                 "flight-delays/parquet/")
    airlines_path = base_path + "airlines"

    @onlyIntegrationTest
    def test_properties(self, integ_connector: S3Connector):
        assert str(integ_connector) == "S3Connector(root_dir=None)"
        assert integ_connector.name == "s3_connector"
        assert integ_connector.source_type == DataSourceType.S3

    @onlyIntegrationTest
    def test_get_table(self, integ_connector: S3Connector):
        assert integ_connector.has_table(self.airlines_path)
        assert self.airlines_path in integ_connector
        airlines_table = integ_connector[self.airlines_path]
        assert isinstance(airlines_table, SourceTable)

        # Table metadata:
        assert {c.name
                for c in airlines_table.columns
                } == set(['IATA_CODE', 'AIRLINE'])

        # Table data:
        df = airlines_table.head(num_rows=7)
        assert isinstance(df, pd.DataFrame)
        assert set(df.columns) == set([c.name for c in airlines_table.columns])
        assert len(df) == 7
