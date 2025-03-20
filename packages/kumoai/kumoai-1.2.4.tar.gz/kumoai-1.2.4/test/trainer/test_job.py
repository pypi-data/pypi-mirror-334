from unittest import mock

import pytest
from kumoapi.jobs import (
    BigQueryPredictionOutput,
    PredictionArtifactType,
    WriteMode,
)

from kumoai import BigQueryConnector
from kumoai.trainer.job import (
    ArtifactExportJob,
    BatchPredictionJobResult,
    OutputConfig,
)


def test_export():
    job_id = "bp-job-123"
    with mock.patch("kumoai.connector.bigquery_connector.global_state",
                    new=mock.MagicMock()) as mock_global:
        mock_global.client.connector_api.create_if_not_exist.return_value = (
            None)
        output_config = OutputConfig(
            output_types=["predictions"],
            output_connector=BigQueryConnector('bq', 'project', 'dataset'),
            output_table_name="bp_table",
            output_metadata_fields=["JOB_TIMESTAMP"],
        )

    with mock.patch("kumoai.trainer.job.global_state",
                    new=mock.MagicMock()) as mock_global:
        # Patch global_state as a MagicMock, no autospec
        # Now define any needed chain of attributes
        # so that `global_state.client.artifact_export_api.create` works.
        mock_global.client.artifact_export_api.create.return_value = \
            "export-job-123"

        job_result = BatchPredictionJobResult(job_id)
        export_job = job_result.export(output_config, non_blocking=True)

        assert isinstance(export_job, ArtifactExportJob)
        assert export_job.id == "export-job-123"
        mock_global.client.artifact_export_api.create.assert_called_once()
        args, _ = mock_global.client.artifact_export_api.create.call_args
        assert args[0].job_id == 'bp-job-123'
        assert isinstance(args[0].prediction_output, BigQueryPredictionOutput)
        output = args[0].prediction_output
        assert output.write_mode == WriteMode.OVERWRITE
        assert output.connector_id == 'bq'
        assert output.artifact_type == PredictionArtifactType.PREDICTIONS
        assert output.table_name == 'bp_table_predictions'
        assert output.extra_fields[0] == 'JOB_TIMESTAMP'


def test_export_with_multiple_prediction_output():
    job_id = "bp-job-123"
    with mock.patch("kumoai.connector.bigquery_connector.global_state",
                    new=mock.MagicMock()) as mock_global:
        mock_global.client.connector_api.create_if_not_exist.return_value = (
            None)
        output_config = OutputConfig(
            output_types=["predictions", "embeddings"],
            output_connector=BigQueryConnector('bq', 'project', 'dataset'),
            output_table_name="bp_table",
            output_metadata_fields=["JOB_TIMESTAMP"],
        )

    with pytest.raises(ValueError) as err:
        with mock.patch("kumoai.trainer.job.global_state",
                        new=mock.MagicMock()) as mock_global:
            # Patch global_state as a MagicMock, no autospec
            # Now define any needed chain of attributes
            # so that `global_state.client.artifact_export_api.create` works.
            mock_global.client.artifact_export_api.create.return_value = \
                "export-job-123"

            job_result = BatchPredictionJobResult(job_id)
            job_result.export(output_config, non_blocking=True)
    assert err is not None
    assert err.value.args[0].startswith(
        'Each export request can only support one output_type')
    assert "['predictions', 'embeddings']" in err.value.args[0]
