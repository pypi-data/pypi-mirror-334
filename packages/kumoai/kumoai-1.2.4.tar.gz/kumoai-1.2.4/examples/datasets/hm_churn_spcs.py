"""H&M Churn on Kumo SDK + SPCS

- Connects to Snowflake
- Runs lightweight pre-processing in SQL
- Runs a typical training process
- Exports the test outcome to the data platform
- Run post processing / custom metric computation in Snowpark

Requirements:
    * Modify `API_URL` and please be sure to set the SNOWFLAKE_USER,
    * SNOWFLAKE_USER, SNOWFLAKE_PASSWORD,
    and SNOWFLAKE_ACCOUNT environment variables.
"""
import os

import snowflake.connector
import snowflake.snowpark.functions as snow_func
from snowflake.snowpark import Session
from snowflake.snowpark.window import Window

import kumoai as kumo
from kumoai.trainer.config import OutputConfig

API_URL = "http://localhost:10002"

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

# Create a connector to a backing data store:
connector = kumo.SnowflakeConnector(
    name="HM",
    account=SNOWFLAKE_ACCOUNT,
    warehouse="KUMO_XS",
    database="KUMO",
    schema_name="HM_SAMPLED",
)

# Connect tables, let Kumo infer all metadata:
customers_src = connector.table("CUSTOMERS")
customers = kumo.Table(
    source_table=customers_src,
    primary_key="CUSTOMER_ID",
    columns=customers_src.columns,
).infer_metadata()

articles_src = connector.table("ARTICLES")
articles = kumo.Table(
    source_table=articles_src,
    primary_key="ARTICLE_ID",
    columns=articles_src.columns,
).infer_metadata()

session = snowflake.connector.connect(
    user=SNOWFLAKE_USER,
    password=SNOWFLAKE_PASSWORD,
    account=SNOWFLAKE_ACCOUNT,
    database="KUMO",
    schema="HM_SAMPLED",
    warehouse="KUMO_XS",
)

# Create an entity table where primary key is the concatenation of customer_id
# and sales_channel_id.
sql = """
    CREATE OR REPLACE TABLE entities AS
    SELECT CONCAT(customer_id, sales_channel_id) AS pk, *
    FROM customers
    CROSS JOIN (SELECT DISTINCT sales_channel_id FROM transactions)
"""
session.cursor().execute(sql)
print("Entities table created.")

# Create a processed transactions table where foreign key is the concatenation
# of customer_id and sales_channel_id.
sql = """
    CREATE OR REPLACE TABLE transactions_processed AS
    SELECT *, CONCAT(customer_id, sales_channel_id) AS fk
    FROM transactions
"""
session.cursor().execute(sql)
print("Transactions processed table created.")

entities_src = connector.table("ENTITIES")
entities = kumo.Table(
    source_table=entities_src,
    primary_key="PK",
    columns=entities_src.columns,
).infer_metadata()

transactions_src = connector.table("TRANSACTIONS_PROCESSED")
transactions = kumo.Table(
    source_table=transactions_src,
    time_column="T_DAT",
    columns=transactions_src.columns,
).infer_metadata()

# Define graph:
graph = kumo.Graph(
    tables={
        'CUSTOMERS': customers,
        'ARTICLES': articles,
        'TRANSACTIONS': transactions,
        'ENTITIES': entities,
    },
    edges=[
        dict(src_table='TRANSACTIONS', fkey='CUSTOMER_ID',
             dst_table='CUSTOMERS'),
        dict(src_table='TRANSACTIONS', fkey='ARTICLE_ID',
             dst_table='ARTICLES'),
        dict(src_table='TRANSACTIONS', fkey='FK', dst_table='ENTITIES'),
    ],
)

# Create predictive query:
pquery = kumo.PredictiveQuery(
    name="churn_sales_channel",
    graph=graph,
    query="""
        PREDICT COUNT(TRANSACTIONS.*, 0, 28, DAYS) = 0 FOR EACH ENTITIES.PK
    """,
)

# Generate training table (blocking is default):
train_table = pquery.generate_training_table()

# Train!
model_plan = pquery.suggest_model_plan()
model_plan.training_job.num_experiments = 1

trainer = kumo.Trainer(model_plan)
training_job = trainer.fit(
    graph=graph,
    train_table=train_table,
)
print(f"Training metrics: {training_job.metrics()}")

# Generate prediction table:
pred_table = pquery.generate_prediction_table()

# Predict!
# TODO(zeyuan): Use holdout set instead of pred table for this:
prediction_job = trainer.predict(
    graph=graph,
    prediction_table=pred_table,
    output_config=OutputConfig(
        output_types={'predictions', 'embeddings'},
        output_connector=connector,
        output_table_name='kumo_bp',
    ),
    training_job_id=training_job.job_id,
    binary_classification_threshold=0.5,
)

# Create snowpark session to later operate on snowpark dataframes:
conn_params = {
    'user': SNOWFLAKE_USER,
    'password': SNOWFLAKE_PASSWORD,
    'account': SNOWFLAKE_ACCOUNT,
    'database': "KUMO",
    'schema': "HM_SAMPLED",
    'warehouse': "KUMO_XS",
}
snowpark_session = Session.builder.configs(conn_params).create()
df = snowpark_session.table("\"kumo_bp_predictions\"")

# Select relevant columns:
df = df.select(
    snow_func.substr("ENTITY", 65, 1).alias("SALES_CHANNEL_ID"),
    snow_func.col("TARGET_PRED").cast("INT").alias("TARGET_PRED"),
    snow_func.col("TRUE_PROB"),
)

# Get top 1000 predictions per sales channel:
ranked_scores = df.with_column(
    "RN",
    snow_func.row_number().over(
        Window.partitionBy("SALES_CHANNEL_ID").orderBy(
            snow_func.desc("TRUE_PROB"))))
ranked_scores = ranked_scores[ranked_scores["RN"] <= 1000]

# Get total predictions per sales channel:
tp_per_channel = ranked_scores.groupBy("SALES_CHANNEL_ID").sum(
    ranked_scores["TARGET_PRED"]).rename("SUM(TARGET_PRED)", "TP")
total_per_channel = df.groupBy("SALES_CHANNEL_ID").sum("TARGET_PRED")
total_per_channel = total_per_channel.rename("SUM(TARGET_PRED)", "TOTAL")

# Compute recall@1000:
final_metrics = tp_per_channel.join(total_per_channel, on="SALES_CHANNEL_ID")
final_metrics = final_metrics.withColumn(
    "RECALL@1000", final_metrics['TP'] / final_metrics['TOTAL'])
print(final_metrics.to_pandas())
