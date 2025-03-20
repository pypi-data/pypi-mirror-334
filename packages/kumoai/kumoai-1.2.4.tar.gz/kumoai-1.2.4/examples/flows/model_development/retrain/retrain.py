"""A demonstration of the ability to retrain an existing model on a new/clean
Python session, in the Kumo SDK. This script simply trains the model.

Requirements:
    * Modify `API_URL` and `API_KEY` to point to a live, appropriate instance
    * Run `train.py` first to obtain a valid job ID that can be used for
        re-training.
"""
import os.path as osp

import kumoai as kumo

API_URL = "http://localhost:10002"
API_KEY = "test:DISABLED"

# Shared location to store model ID:
path = osp.join(osp.dirname(osp.realpath(__file__)), "training_job")
with open(path, "r") as f:
    job_id = f.readlines()[0].strip('\n')

kumo.init(url=API_URL, api_key=API_KEY)

# Load and Re-Train in New Session ############################################

# Load the trainer from the job ID:
trainer_loaded = kumo.Trainer.load(job_id)
print(f"Loaded trainer for job {job_id} with configuration {trainer_loaded}")

# Load the predictive query from its name.
#
# NOTE this will change very soon, to be
# kumo.Trainer.load_predictive_query(job_id), as we are transitioning to
# deep-copying a predictive query into Trainer:
pq_loaded = kumo.PredictiveQuery.load_from_training_job(job_id)

# Force re-snapshot the graph to obtain the latest data:
pq_loaded.graph.snapshot(force_refresh=True)

# Modify one part of the loaded plan:
trainer_loaded_plan = trainer_loaded.model_plan
trainer_loaded_plan.model_architecture.channels = [32]

print(f"Fitting loaded trainer with modified model plan {trainer_loaded_plan}")
trainer_loaded.fit(
    graph=pq_loaded.graph,
    train_table=pq_loaded.generate_training_table(non_blocking=True),
    non_blocking=False,
)
