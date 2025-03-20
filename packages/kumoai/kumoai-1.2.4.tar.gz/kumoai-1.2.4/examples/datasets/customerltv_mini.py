"""CustomerLTV Mini (Toy Dataset) on Kumo SDK.

Requirements:
    * Modify `API_URL` and `API_KEY` to point to a live, appropriate instance
    * If running in SPCS, please be sure to set the SNOWFLAKE_USER,
        SNOWFLAKE_PASSWORD, and SNOWFLAKE_ACCOUNT environment variables.
"""
import argparse
import os

import kumoai as kumo
from kumoai.encoder import GloVe
from kumoai.pquery import PredictionTable
from kumoai.trainer.config import OutputConfig

parser = argparse.ArgumentParser()
parser.add_argument('--spcs', type=bool, default=False)
parser.add_argument('--training_job_id', type=str, default='')
parser.add_argument(
    '--export_loc', type=str, default='s3', choices=['s3', 'snow', 'db'],
    help='Export location for prediction table'
    'See `export_connector`` in the script to see'
    'exact location.')
args = parser.parse_args()

API_URL = "http://localhost:10002"
API_KEY = "test:DISABLED"

# Initialize the Kumo SDK:
if args.spcs:
    SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
    SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
    SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
    assert SNOWFLAKE_USER and SNOWFLAKE_PASSWORD and SNOWFLAKE_ACCOUNT

    credentials = {
        "user": SNOWFLAKE_USER,
        "password": SNOWFLAKE_PASSWORD,
        "account": SNOWFLAKE_ACCOUNT,
    }
    kumo.init(url=API_URL, snowflake_credentials=credentials)
else:
    kumo.init(url=API_URL, api_key=API_KEY)

# Create a connector to a backing data store:
if args.spcs:
    connector = kumo.SnowflakeConnector(
        name="COMMON_ID",
        account=SNOWFLAKE_ACCOUNT,
        warehouse="KUMO_XS",
        database="KUMO",
        schema_name="PUBLIC",
    )
else:
    connector = kumo.S3Connector(
        "s3://kumo-public-datasets/customerltv_mini_integ_test/")

pred_output_table_name = 'customer_ltv_mini'
if args.export_loc == 's3':
    export_connector = kumo.S3Connector(
        "s3://kumo-public-datasets/customerltv_mini_integ_test/")
elif args.export_loc == 'snow':
    export_connector = kumo.SnowflakeConnector(
        name="COMMON_ID",
        account=SNOWFLAKE_ACCOUNT,
        warehouse="KUMO_XS",
        database="KUMO",
        schema_name="PUBLIC",
    )
elif args.export_loc == 'db':
    export_connector = kumo.DatabricksConnector(
        name="COMMON_ID1",
        host="https://dbc-117b701d-939a.cloud.databricks.com",
        cluster_id="0626-191119-75431625",
        warehouse_id="82d859e4a6b283a0",
        catalog="kumo_test_catalogue",
    )
    pred_output_table_name = ('pred_tables', 'customer_ltv_mini')

# Metadata ####################################################################

customer_table = "customer"
customer_id = "CustomerID"
stock_table = "stock"
stock_code = "StockCode"
transaction_table = "transaction"
invoice_date = "InvoiceDate"
quantity = "Quantity"
unit_price = "UnitPrice"
if args.spcs:
    customer_table = customer_table.upper()
    customer_id = customer_id.upper()
    stock_table = stock_table.upper()
    stock_code = stock_code.upper()
    transaction_table = 'TRANSACTION_DATEFORMATS'
    # use the column with YYYYMMDD integers, which requires
    # setting timestamp_format to correctly run:
    invoice_date = 'INVOICEDATE_INT'
    quantity = quantity.upper()
    unit_price = unit_price.upper()

# Training ####################################################################

job_id = args.training_job_id
if job_id == "":
    customer = kumo.Table.from_source_table(
        source_table=connector.table(customer_table),
        primary_key=customer_id,
    ).infer_metadata()
    customer.print_definition()

    stock = kumo.Table.from_source_table(
        source_table=connector.table(stock_table),
        primary_key=stock_code,
    ).infer_metadata()
    stock.print_definition()

    transaction = kumo.Table.from_source_table(
        source_table=connector.table(transaction_table),
        time_column=invoice_date,
    ).infer_metadata()
    transaction['Description'].stype = kumo.Stype.text
    transaction[invoice_date].dtype = kumo.Dtype.time
    transaction.print_definition()

    # Override, as an example:
    if args.spcs:
        transaction[invoice_date].timestamp_format = 'YYYYMMDD'

    # Define graph:
    graph = kumo.Graph(
        tables={
            customer_table: customer,
            stock_table: stock,
            transaction_table: transaction,
        },
        edges=[
            dict(src_table=transaction_table, fkey=stock_code,
                 dst_table=stock_table),
            dict(src_table=transaction_table, fkey=customer_id,
                 dst_table=customer_table),
        ],
    )
    graph.validate()

    # Save graph as template for the future. The graph can then be loaded with
    #   >> graph = kumo.Graph.load('customerltv_graph')
    # graph.save('customerltv_graph')

    # Create predictive query:
    pquery = kumo.PredictiveQuery(
        graph=graph,
        query=(
            f"PREDICT MAX({transaction_table}.{quantity}, 0, 30)\n"
            f"FOR EACH {customer_table}.{customer_id}\n"
            f"ASSUMING SUM({transaction_table}.{unit_price}, 0, 7, days) > 15"
        ),
    )
    print(f"Task type: {pquery.get_task_type()}")

    # Save PQ as template for the future. The PQ can then be loaded with
    #   >> pquery = kumo.PredictiveQuery.load('customerltv_pquery')
    # pquery.save('customerltv_pquery')

    # Snapshot graph, wait for it to finish. Note that this is not a necessary
    # step in the pipeline:
    snapshot_id = graph.snapshot(non_blocking=False, force_refresh=True)

    # Get edge health stats, which should be ready by now since we are blocking
    # on the snapshot
    edge_health = graph.get_edge_stats(non_blocking=False)
    print(f"Edge health: {edge_health}")

    full_stats = graph.get_table_stats(wait_for="full")
    print(f"Full stats: {full_stats}")

    # Generate training table:
    train_table = pquery.generate_training_table(non_blocking=True)

    # Train!
    model_plan = pquery.suggest_model_plan()
    model_plan.training_job.num_experiments = 3
    model_plan.column_processing.encoder_overrides = {
        f'{transaction_table}.Description': GloVe('glove.6B')  # try GloVe...
    }
    print(model_plan)
    trainer = kumo.Trainer(model_plan)
    training_job = trainer.fit(
        graph=graph,
        train_table=train_table,
        non_blocking=False,
    )
    print(f"Training metrics: {training_job.metrics()}")
    job_id = training_job.job_id

    # Trigger baseline workflow through the following script.
    metrics = model_plan.training_job.metrics
    baseline_job = pquery.generate_baseline(
        train_table=train_table,
        metrics=metrics,
    )
    print(f"Baseline metrics: {baseline_job.metrics()}")

# Inference ###################################################################

print(f"Generating predictions from training job {job_id}")

# Load the training job, PQ, and Graph:
training_job = kumo.TrainingJob(job_id).result()
trainer = kumo.Trainer.load(job_id)
pquery = kumo.PredictiveQuery.load_from_training_job(job_id)
graph = pquery.graph

# Try with new S3 connector, so it has a new FPID:
prediction_connector = kumo.S3Connector(
    's3://kumo-public-datasets/customerltv_mini_integ_test/temp/')
graph['customer'].source_table = prediction_connector['customer']

# Use a new predictive query, which will show a warning but will
# work:
pquery = kumo.PredictiveQuery(
    graph=graph,
    query=(f"PREDICT MAX({transaction_table}.{quantity}, 0, 30)\n"
           f"FOR EACH {customer_table}.{customer_id}\n"),
)

# Predict!
pred_table = pquery.generate_prediction_table(non_blocking=True)
prediction_job = trainer.predict(
    graph=graph,
    prediction_table=pred_table,
    output_config=OutputConfig(
        output_connector=connector,
        output_types={'predictions', 'embeddings'},
        output_table_name='kumo_predictions',
        output_metadata_fields=['JOB_TIMESTAMP'],
    ),
    training_job_id=training_job.job_id,
    non_blocking=False,
)
print(f'Batch prediction job summary: {prediction_job.summary()}')

# Export predictions to a separate place:
export_job = prediction_job.export(
    output_type='predictions',
    output_connector=export_connector,
    output_table_name=pred_output_table_name,
    output_metadata_fields=['JOB_TIMESTAMP'],
    non_blocking=False,
)
print(f'Export artifact job {export_job}')

# Custom Inference ############################################################

pred_table_df = pred_table.result().data_df()

if args.spcs:
    # Create custom prediction table in Snowflake:
    import snowflake.snowpark as snowpark
    assert isinstance(pred_table_df, snowpark.DataFrame)
    custom_pred_table_df = pred_table_df.sample(n=100)
    custom_pred_table_path = "@kumo_app.kumo_app_schema." + \
        "local_stage/custom_pred_table.parquet/"
    custom_pred_table_df.write.mode("overwrite").copy_into_location(
        custom_pred_table_path,
        header=True,
        file_format_type="parquet",
        overwrite=True,
    )
else:
    # Create simple custom prediction table and write it out to a path:
    custom_pred_table_df = pred_table_df.head(100).astype(
        {'TIMESTAMP': 'datetime64[ms]'})
    custom_pred_table_path = (
        's3://kumocloud-test-bucket/sdk/custom_pred_table.parquet')
    custom_pred_table_df.to_parquet(custom_pred_table_path)
custom_pred_table = PredictionTable(table_data_path=custom_pred_table_path)
custom_prediction_job = trainer.predict(
    graph=graph,
    prediction_table=custom_pred_table,
    output_config=OutputConfig(
        output_types={'predictions', 'embeddings'},
        output_connector=connector,
        output_table_name='kumo_predictions_custom',
    ),
    training_job_id=training_job.job_id,
    non_blocking=False,
)

print(f'Batch prediction job summary: {custom_prediction_job.summary()}')
