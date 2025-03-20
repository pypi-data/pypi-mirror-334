import kumoai as kumo
from kumoai.trainer.config import OutputConfig


def init(params):
    url = params['kumo_spcs_url']
    credentials = {
        "user": params['snowflake_username'],
        "password": params['snowflake_password'],
        "account": params['snowflake_account'],
    }
    kumo.init(url=url, snowflake_credentials=credentials)


def predict(params):
    job_id = params['kumo_training_job_id']
    pq_name = params['kumo_pq_name']

    # Load the trainer from the job ID:
    trainer_loaded = kumo.Trainer.load(job_id)
    print(f"Loaded trainer for job {job_id}")

    # Load the predictive query from its name.
    pq_loaded = kumo.PredictiveQuery.load(pq_name)

    connector = kumo.SnowflakeConnector(
        name="output_connector",
        account=params['snowflake_account'],
        warehouse=params['snowflake_warehouse'],
        database=params['snowflake_database'],
        schema_name=params['snowflake_schema'],
    )

    job = trainer_loaded.predict(
        graph=pq_loaded.graph,
        prediction_table=pq_loaded.generate_prediction_table(
            non_blocking=True),
        output_config=OutputConfig(
            output_types={'predictions', 'embeddings'},
            output_connector=connector,
            output_table_name='bp_predictions',
        ),
        training_job_id=job_id,
        binary_classification_threshold=0.5,
    )
    if job.status().status != 'DONE':
        raise RuntimeError("Prediction job failed")

    return job.job_id
