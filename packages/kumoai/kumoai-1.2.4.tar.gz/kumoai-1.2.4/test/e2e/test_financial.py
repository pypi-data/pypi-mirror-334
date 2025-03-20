import time

from kumoapi.model_plan import RunMode

from kumoai.connector import S3Connector
from kumoai.connector.source_table import SourceTable
from kumoai.graph import Graph, Table
from kumoai.pquery import PredictiveQuery
from kumoai.pquery.prediction_table import PredictionTable, PredictionTableJob
from kumoai.testing import onlyIntegrationTest
from kumoai.trainer.config import OutputConfig
from kumoai.trainer.job import BatchPredictionJobResult
from kumoai.trainer.trainer import Trainer


class TestFinancialS3:
    r"""Tests a common user workflow when creating predictive queries on the
    publicly-available Financial dataset hosted on S3.
    """
    dataset_directory = "s3://kumo-public-datasets/financial/parquet/"

    @onlyIntegrationTest
    def test_source_tables(self, setup_integration_client):
        connector = S3Connector(self.dataset_directory)

        # Ensure you can load source data as `SourceTable`s:
        for table_name in ['ACCOUNT', 'LOAN', 'TRANS']:
            source_table = connector[table_name]
            assert all([col.name for col in source_table.columns] ==
                       source_table.head().columns)

    @onlyIntegrationTest
    def test_tables(self, setup_integration_client):
        connector = S3Connector(self.dataset_directory)

        # Create tables:
        # TODO(manan): use `infer_metadata`
        # TODO(manan): use dtype and stype adjustments
        account = Table.from_source_table(
            connector['ACCOUNT'],
            column_names=['FREQUENCY', 'DATE', 'DISTRICT_ID'],
            primary_key='ACCOUNT_ID',
        ).infer_metadata()
        assert len(account.columns) == 4
        assert account.primary_key.name == 'ACCOUNT_ID'

        loan = Table.from_source_table(
            connector['LOAN'],
            column_names=[
                'AMOUNT', 'DURATION', 'PAYMENTS', 'STATUS', 'ACCOUNT_ID'
            ],
            primary_key='LOAN_ID',
            time_column='DATE',
        ).infer_metadata()
        assert len(loan.columns) == 7
        assert loan.primary_key.name == 'LOAN_ID'
        assert loan.time_column.name == 'DATE'

        trans = Table.from_source_table(
            connector['TRANS'],
            column_names=[
                'TYPE', 'OPERATION', 'AMOUNT', 'BALANCE', 'K_SYMBOL',
                'ACCOUNT_ID', 'TRANS_ID', 'DATE'
            ],
            primary_key='TRANS_ID',
            time_column='DATE',
        ).infer_metadata()
        assert len(trans.columns) == 8
        assert trans.primary_key.name == 'TRANS_ID'
        assert trans.time_column.name == 'DATE'

        # Save state for graph test:
        TestFinancialS3.tables = [account, loan, trans]

    @onlyIntegrationTest
    def test_graph(self, setup_integration_client):
        account, loan, trans = TestFinancialS3.tables

        graph = Graph({'ACCOUNT': account, 'LOAN': loan, 'TRANS': trans})
        graph.link('LOAN', 'ACCOUNT_ID', 'ACCOUNT')
        graph.link('TRANS', 'ACCOUNT_ID', 'ACCOUNT')

        assert 'ACCOUNT' in graph
        graph_id = graph.save()
        assert graph_id == 'graph-554a93dae99de532ff11d8999b2234f9'
        graph.save('test_financial_graph')
        assert graph.id == Graph.load('test_financial_graph').id

    @onlyIntegrationTest
    def test_training(self, setup_integration_client):
        graph = Graph.load('test_financial_graph')
        query = """
PREDICT SUM(LOAN.AMOUNT, 0, 180, days)
FOR EACH ACCOUNT.ACCOUNT_ID
"""
        pquery = PredictiveQuery(graph, query)
        pquery_id = pquery.save()
        assert pquery_id == 'pquery-3d742847ee3b6b0e9bfcae85388ece6c'
        pquery.save('test_pquery_name')
        assert PredictiveQuery.load('test_pquery_name').id == pquery_id
        train_table = pquery.generate_training_table()

        trainer = Trainer(pquery.suggest_model_plan(run_mode=RunMode.DEBUG))
        training_job = trainer.fit(graph, train_table)
        TestFinancialS3.model_id = training_job.job_id

    @onlyIntegrationTest
    def test_prediction(self, setup_integration_client):
        if hasattr(TestFinancialS3, 'model_id'):
            trainer = Trainer.load(TestFinancialS3.model_id)
        else:
            trainer = Trainer.load_from_tags(
                {'pquery_id': 'pquery-3d742847ee3b6b0e9bfcae85388ece6c'})
        pquery = PredictiveQuery.load_from_training_job(
            trainer._training_job_id)

        pred_table = pquery.generate_prediction_table()
        TestFinancialS3.pred_table_job_id = pred_table.job_id
        s3_output_dir = ('s3://kumo-dev-dataplane-bucket/sdk_integ_tests/'
                         f'output_{int(time.time())}')
        output_connector = S3Connector(s3_output_dir)
        output_table_name = 'test_prediction'
        output_config = OutputConfig(
            output_connector=output_connector,
            output_table_name=output_table_name,
            output_types=['predictions'],
        )

        pred_job: BatchPredictionJobResult = trainer.predict(
            graph=pquery.graph,
            prediction_table=pred_table,
            output_config=output_config,
        )
        assert pred_job.summary().num_entities_predicted == 4500

        output_table_name += '_predictions'
        assert output_connector.has_table(output_table_name)
        output_table = SourceTable(output_table_name, output_connector)
        assert [col.name
                for col in output_table.columns] == ['ENTITY', 'TARGET_PRED']

    @onlyIntegrationTest
    def test_custom_prediction_table(self, setup_integration_client):
        if hasattr(TestFinancialS3, 'model_id'):
            trainer = Trainer.load(TestFinancialS3.model_id)
        else:
            trainer = Trainer.load_from_tags(
                {'pquery_id': 'pquery-3d742847ee3b6b0e9bfcae85388ece6c'})
        pquery = PredictiveQuery.load_from_training_job(
            trainer._training_job_id)

        pred_table_fut = PredictionTableJob(TestFinancialS3.pred_table_job_id)
        # Simulate "custom-processing" of prediction table.
        pred_table_df = pred_table_fut.result().data_df()
        custom_pred_table_df = pred_table_df.head(100).astype(
            {'TIMESTAMP': 'datetime64[ms]'})
        custom_pred_table_path = (
            f's3://kumo-dev-dataplane-bucket/sdk_integ_tests/'
            f'{int(time.time())}/custom_pred_table.parquet')
        custom_pred_table_df.to_parquet(custom_pred_table_path)

        # Use the custom prediction table to make prediction.
        custom_pred_table = PredictionTable(
            table_data_path=custom_pred_table_path)
        s3_output_dir = ('s3://kumo-dev-dataplane-bucket/sdk_integ_tests/'
                         f'output_{int(time.time())}')
        output_connector = S3Connector(s3_output_dir)
        output_table_name = 'test_custom_prediction'
        pred_job: BatchPredictionJobResult = trainer.predict(
            graph=pquery.graph,
            prediction_table=custom_pred_table,
            output_config=OutputConfig(
                output_connector=output_connector,
                output_types=set(['predictions']),
                output_table_name=output_table_name,
            ),
        )
        assert pred_job.summary().num_entities_predicted == 100
        output_table_name += '_predictions'
        assert output_connector.has_table(output_table_name)
        output_table = SourceTable(output_table_name, output_connector)
        assert [col.name
                for col in output_table.columns] == ['ENTITY', 'TARGET_PRED']
