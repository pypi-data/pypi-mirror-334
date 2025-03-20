"""H&M recommendation with LLM embedded articles table by using Kumo SDK.

Requirements:
    * Modify `API_URL` and `API_KEY` to point to a live, appropriate instance
    * Modify `OUTPUT_DIR` and `OPENAI_API_KEY` to run LLM embedding job
"""
import time

from kumoapi.jobs import JobStatus

import kumoai as kumo
from kumoai.graph import Table

API_URL = "http://localhost:10002"
API_KEY = "test:DISABLED"
OUTPUT_DIR = "REPLACE"
OPENAI_API_KEY = "REPLACE"

# Initialize the Kumo SDK:
kumo.init(api_key=API_KEY, url=API_URL)

connector = kumo.S3Connector(
    root_dir="s3://kumo-public-datasets/Kaggle_H&M/parquet/")

customers_src = connector.table("customers")
customers = kumo.Table(
    source_table=customers_src,
    primary_key="customer_id",
    columns=customers_src.columns,
).infer_metadata()

articles_src_future = connector["articles"].add_llm(
    model="text-embedding-3-small",
    api_key=OPENAI_API_KEY,
    template=("The product {prod_name} in the {section_name} section"
              "is categorized as {product_type_name} "
              "and has following description: {detail_desc}"),
    output_dir=OUTPUT_DIR,
    output_column_name="embedding_column",
    output_table_name="articles_emb",
    dimensions=256,
    non_blocking=True,
)

print(f"LLM embedding job ID: {articles_src_future.job_id}")
while articles_src_future.status() == JobStatus.RUNNING:
    print(f"LLM embedding status {time.ctime()}: "
          f"{articles_src_future.status()}")
    time.sleep(2)

# You can cancel the job by:
# resp = articles_src_future.cancel()
# print(f"Cancel job {articles_src_future.job_id}: {resp}")

articles_src = articles_src_future.result()

articles = Table.from_source_table(
    source_table=articles_src,
    primary_key="article_id",
).infer_metadata()

transactions_src = connector.table("transactions_train")
transactions = kumo.Table(
    source_table=transactions_src,
    time_column="t_dat",
    columns=transactions_src.columns,
).infer_metadata()

# Define graph:
graph = kumo.Graph(
    tables={
        'customers': customers,
        'articles': articles,
        'transactions': transactions,
    },
    edges=[
        dict(src_table='transactions', fkey='customer_id',
             dst_table='customers'),
        dict(src_table='transactions', fkey='article_id',
             dst_table='articles'),
    ],
)

# Create predictive query:
pquery = kumo.PredictiveQuery(
    name="filtered_hnm_rec_sdk",
    graph=graph,
    query="""
        PREDICT LIST_DISTINCT(transactions.article_id, 0, 60, days) RANK TOP 10
        FOR EACH customers.customer_id
    """,
)

# Generate training table (blocking is default):
train_table = pquery.generate_training_table()

# Train!
model_plan = pquery.suggest_model_plan()
model_plan.training_job.num_experiments = 1
model_plan.optimization.batch_size = [128]

trainer = kumo.Trainer(model_plan)
training_job = trainer.fit(
    graph=graph,
    train_table=train_table,
    non_blocking=False,
)
print(f"Training metrics: {training_job.metrics()}")
