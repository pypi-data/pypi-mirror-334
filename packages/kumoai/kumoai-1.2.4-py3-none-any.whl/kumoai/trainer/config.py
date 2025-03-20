from dataclasses import dataclass
from typing import List, Optional, Set, Tuple, Union

from kumoapi.jobs import MetadataField, WriteMode
from pydantic import validator

from kumoai.connector.base import Connector


@dataclass(frozen=True)
class BigQueryOutputConfig:
    # If using OVERWRITE, big query connector will first write to a staging
    # table followed by overwriting to the destination table.
    write_mode: WriteMode = WriteMode.APPEND


CONNECTOR_CONFIG_MAPPING = {
    'BigQueryConnector': BigQueryOutputConfig,
    # Add other mappings as they become available
    # 'DatabricksConnector': DatabricksOutputConfig,
    # 'S3Connector': S3OutputConfig,
    # 'SnowflakeConnector': SnowflakeConnectorConfig,
}


@dataclass(frozen=True)
class OutputConfig:
    """
    Output configuration associated with a Batch Prediction Job.

    Args:
        output_types: The types of outputs that should be produced by
            the prediction job. Can include either ``'predictions'``,
            ``'embeddings'``, or both.
        output_connector: The output data source that Kumo should write
                batch predictions to, if it is None, produce local download
                output only.
        output_table_name: The name of the table in the output data source
            that Kumo should write batch predictions to. In the case of
            a Databricks connector, this should be a tuple of two strings:
            the schema name and the output prediction table name.
        output_metadata_fields: Any additional metadata fields to include
            as new columns in the produced ``'predictions'`` output.
            Currently, allowed options are ``JOB_TIMESTAMP`` and
            ``ANCHOR_TIMESTAMP``.
        connector_specific_config: Defines custom connector specific output
            config for predictions, for example whether to append or overwrite
            existing table.
    """
    output_types: Set[str]
    output_connector: Optional[Connector] = None
    output_table_name: Optional[Union[str, Tuple]] = None
    output_metadata_fields: Optional[List[MetadataField]] = None
    connector_specific_config: Optional[Union[BigQueryOutputConfig]] = None

    @validator('connector_specific_config')
    def validate_connector_config(cls, v, values):  # type: ignore
        # Skip validation if no connector or no specific config
        if values.get('output_connector') is None or v is None:
            return v

        connector_type = type(values['output_connector']).__name__
        expected_config_type = CONNECTOR_CONFIG_MAPPING.get(connector_type)

        # If we don't have a mapping for this connector type, it doesn't
        # support specific configs yet
        if expected_config_type is None:
            raise ValueError(
                f"Connector type '{connector_type}' does not support "
                f"specific output configurations")

        # Check if the provided config is of the correct type
        if not isinstance(v, expected_config_type):
            raise ValueError(
                f"Connector type '{connector_type}' requires output config "
                f"of type '{expected_config_type.__name__}', but got "
                f"'{type(v).__name__}'")

        return v
