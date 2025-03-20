from __future__ import annotations

import asyncio
import logging
import time
from concurrent.futures import Future
from typing import List, Mapping, Optional, Tuple

import pandas as pd
from kumoapi.common import JobStatus
from kumoapi.jobs import (
    CustomTrainingTable,
    GenerateTrainTableJobResource,
    JobStatusReport,
    TrainingTableSpec,
)
from tqdm.auto import tqdm
from typing_extensions import Self, override

from kumoai import global_state
from kumoai.client.jobs import (
    GenerateTrainTableJobAPI,
    GenerateTrainTableJobID,
)
from kumoai.connector import SourceTable
from kumoai.formatting import pretty_print_error_details
from kumoai.futures import KumoProgressFuture, create_future

logger = logging.getLogger(__name__)


class TrainingTable:
    r"""A training table in the Kumo platform. A training table can be
    initialized from a job ID of a completed training table generation job.

    .. code-block:: python

        import kumoai

        # Create a Training Table from a training table generation job. Note
        # that the job ID passed here must be in a completed state:
        training_table = kumoai.TrainingTable("gen-traintable-job-...")

        # Read the training table as a Pandas DataFrame:
        training_df = training_table.data_df()

        # Get URLs to download the training table:
        training_download_urls = training_table.data_urls()

    Args:
        job_id: ID of the training table generation job which generated this
            training table.
    """
    def __init__(self, job_id: GenerateTrainTableJobID):
        self.job_id = job_id
        status = _get_status(job_id).status
        self._custom_train_table: Optional[CustomTrainingTable] = None
        if status != JobStatus.DONE:
            raise ValueError(
                f"Job {job_id} is not yet complete (status: {status}). If you "
                f"would like to create a future (waiting for training table "
                f"generation success), please use `TrainingTableJob`.")

    def data_urls(self) -> List[str]:
        r"""Returns a list of URLs that can be used to view generated
        training table data. The list will contain more than one element
        if the table is partitioned; paths will be relative to the location of
        the Kumo data plane.
        """
        api: GenerateTrainTableJobAPI = (
            global_state.client.generate_train_table_job_api)
        return api._get_table_data(self.job_id, presigned=True, raw_path=True)

    def data_df(self) -> pd.DataFrame:
        r"""Returns a :class:`~pandas.DataFrame` object representing the
        generated training data.

        .. warning::

            This method will load the full training table into memory as a
            :class:`~pandas.DataFrame` object. If you are working on a machine
            with limited resources, please use
            :meth:`~kumoai.pquery.TrainingTable.data_urls` instead to download
            the data and perform analysis per-partition.
        """
        urls = self.data_urls()
        if global_state.is_spcs:
            from kumoai.spcs import _parquet_dataset_to_df

            # TODO(dm): return type hint is wrong
            return _parquet_dataset_to_df(self.data_urls())

        try:
            return pd.concat([pd.read_parquet(x) for x in urls])
        except Exception as e:
            raise ValueError(
                f"Could not create a Pandas DataFrame object from data paths "
                f"{urls}. Please construct the DataFrame manually.") from e

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(job_id={self.job_id})'

    def validate_custom_table(self, source_table: SourceTable,
                              train_table_mod: TrainingTableSpec) -> None:
        r"""Validates the modified training table.

        Args:
            source_table (SourceTable): The source table to be used as the
                modified training table.
            train_table_mod (TrainTableSpec): The modification specification.

        Raises:
            ValueError: If the modified training table is invalid.

        """

        api: GenerateTrainTableJobAPI = (
            global_state.client.generate_train_table_job_api)
        response = api.validate_custom_train_table(
            self.job_id, source_table._to_api_source_table(), train_table_mod)
        if not response.ok:
            raise ValueError("Invalid weighted train table",
                             response.error_message)

    def update(
        self,
        source_table: SourceTable,
        train_table_mod: TrainingTableSpec,
        validate: bool = True,
    ) -> Self:
        r"""Sets the `source_table` as the modified training table.

        .. note::
            The only allowed modification is the addition of weight column
            Any other modification might lead to unintentded ERRORS downstream.

        The custom training table is ingested during trainer.fit()
        and is used as the training table.

        Args:
            source_table (SourceTable): The source table to be used as the
                modified training table.
            table_mod_spec (TrainTableSpec): The modification specification.
            validate (bool): Whether to validate the modified training table.
                This can be slow for large tables.

        """
        if validate:
            self.validate_custom_table(source_table, train_table_mod)
        self._custom_train_table = CustomTrainingTable(
            source_table=source_table._to_api_source_table(),
            table_mod_spec=train_table_mod, validated=validate)
        return self


# Training Table Future #######################################################


class TrainingTableJob(KumoProgressFuture[TrainingTable]):
    r"""A representation of an ongoing training table generation job in the
    Kumo platform.

    .. code-block:: python

        import kumoai

        # See `PredictiveQuery` documentation:
        pquery = kumoai.PredictiveQuery(...)

        # If a training table is generated in nonblocking mode, the response
        # will be of type `TrainingTableJob`:
        training_table_job = pquery.generate_training_table(non_blocking=True)

        # You can also construct a `TrainingTableJob` from a job ID, e.g.
        # one that is present in the Kumo Jobs page:
        training_table_job = kumoai.TrainingTableJob("trainingjob-...")

        # Get the status of the job:
        print(training_table_job.status())

        # Attach to the job, and poll progress updates:
        training_table_job.attach()

        # Cancel the job:
        training_table_job.cancel()

        # Wait for the job to complete, and return a `TrainingTable`:
        training_table_job.result()

    Args:
        job_id: ID of the training table generation job.
    """
    def __init__(
        self,
        job_id: GenerateTrainTableJobID,
    ) -> None:
        self.job_id = job_id
        # A training table holds a reference to the future that tracks the
        # execution of its generation.
        self._fut: Future[TrainingTable] = create_future(_poll(job_id))

    @property
    def id(self) -> GenerateTrainTableJobID:
        r"""The unique ID of this training table generation process."""
        return self.job_id

    @override
    def result(self) -> TrainingTable:
        return self._fut.result()

    @override
    def future(self) -> Future[TrainingTable]:
        return self._fut

    def status(self) -> JobStatusReport:
        r"""Returns the status of a running training table generation job."""
        return _get_status(self.job_id)

    @override
    def _attach_internal(self, interval_s: float = 4.0) -> TrainingTable:
        assert interval_s >= 4.0
        print(f"Attaching to training table generation job {self.job_id}. "
              f"Tracking this job in the Kumo UI is coming soon. To detach "
              f"from this job, please enter Ctrl+C (the job will continue to "
              f"run, and you can re-attach anytime).")
        api = global_state.client.generate_train_table_job_api

        def _get_progress() -> Optional[Tuple[int, int]]:
            progress = api.get_progress(self.job_id)
            if len(progress) == 0:
                return None
            expected_iter = progress['num_expected_iterations']
            completed_iter = progress['num_finished_iterations']
            return (expected_iter, completed_iter)

        # Print progress bar:
        print("Training table generation is in progress. If your task is "
              "temporal, progress per timeframe will be loaded shortly.")

        # Wait for either timeframes to become available, or the job is done:
        progress = _get_progress()
        while progress is None:
            progress = _get_progress()
            # Not a temporal task, and it's done:
            if self.status().status.is_terminal:
                return self.result()
            time.sleep(interval_s)

        # Wait for timeframes to become available:
        progress = _get_progress()
        assert progress is not None
        total, prog = progress
        pbar = tqdm(total=total, unit="timeframe",
                    desc="Generating Training Table")
        pbar.update(pbar.n - prog)
        while not self.done():
            progress = _get_progress()
            assert progress is not None
            total, prog = progress
            pbar.reset(total)
            pbar.update(prog)
            time.sleep(interval_s)
        pbar.update(pbar.total)
        pbar.close()

        # Future is done:
        return self.result()

    def delete_tags(self, tags: List[str]) -> bool:
        r"""Removes the tags from the job.

        Args:
            tags (List[str]): The tags to remove.
        """
        api = global_state.client.generate_train_table_job_api
        return api.delete_tags(self.job_id, tags)

    def update_tags(self, tags: Mapping[str, Optional[str]]) -> bool:
        r"""Updates the tags of the job.

        Args:
            tags (Mapping[str, Optional[str]]): The tags to update.
                Note that the value 'none' will remove the tag. If the tag is
                not present, it will be added.
        """
        api = global_state.client.generate_train_table_job_api
        return api.update_tags(self.job_id, tags)

    def cancel(self) -> None:
        r"""Cancels a running training table generation job, and raises an
        error if cancellation failed.
        """
        api = global_state.client.generate_train_table_job_api
        return api.cancel(self.job_id)


def _get_status(job_id: str) -> JobStatusReport:
    api = global_state.client.generate_train_table_job_api
    resource: GenerateTrainTableJobResource = api.get(job_id)
    return resource.job_status_report


async def _poll(job_id: str) -> TrainingTable:
    # TODO(manan): make asynchronous natively with aiohttp:
    status = _get_status(job_id).status
    while not status.is_terminal:
        await asyncio.sleep(10)
        status = _get_status(job_id).status

    if status != JobStatus.DONE:
        api = global_state.client.generate_train_table_job_api
        error_details = api.get_job_error(job_id)
        error_str = pretty_print_error_details(error_details)
        raise RuntimeError(
            f"Training table generation for job {job_id} failed with "
            f"job status {status}. Encountered below error(s):"
            f'{error_str}')

    return TrainingTable(job_id)
