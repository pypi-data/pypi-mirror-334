import os
from typing import Dict, Union, Optional
from google.cloud import aiplatform

from .interface import ExperimentLogger, TensorboardLogger

class VertexAIExperimentLogger(ExperimentLogger):
    """
    Concrete implementation of ExperimentLogger for Vertex AI.
    """
    def __init__(self, experiment_name: str) -> None:
        """
        Initialize the Vertex AI Experiment Logger.

        Args:
            experiment_name (str): Name of the experiment in Vertex AI.
        """
        self.experiment_name = experiment_name
        self.project_id = os.getenv("SMLP_PROJECT_ID")
        self.location = os.getenv("SMLP_REGION")
        self.tensorboard_id = os.getenv("SMLP_TENSORBOARD_ID")

        aiplatform.init(
            project=self.project_id,
            location=self.location,
            experiment=self.experiment_name,
            experiment_tensorboard=(
                f"projects/{self.project_id}/locations/{self.location}/tensorboards/{self.tensorboard_id}"
            )
        )

    def start_run(self, run_name: str, existing_run: bool = False) -> None:
        """
        Start a new run in Vertex AI Experiment.

        Args:
            run_name (str): Name of the run.
            existing_run (bool): Whether to resume an existing run.

        Returns:
            None
        """
        aiplatform.start_run(run=run_name, resume=existing_run)

    def end_run(self) -> None:
        """
        End the current run in Vertex AI Experiment.

        Returns:
            None
        """
        aiplatform.end_run()

    def log_metrics(self, metrics: Dict[str, float], step: Optional[int]) -> None:
        """
        Log time series metrics to Vertex AI Experiment.

        Args:
            metrics (Dict[str, float]): Dictionary containing metrics.
            step (Optional[int]): Training step.

        Returns:
            None
        """
        aiplatform.log_time_series_metrics(metrics=metrics, step=step)

    def log_params(self, params: Dict[str, Union[float, int, str]]) -> None:
        """
        Log hyperparameters to Vertex AI Experiment.

        Args:
            params (Dict[str, Union[float, int, str]]): Dictionary containing hyperparameters.

        Returns:
            None
        """
        aiplatform.log_params(params)

class VertexAITensorboardLogger(TensorboardLogger):
    """
    Concrete implementation of TensorboardLogger for Vertex AI.
    """
    def __init__(self, log_dir: str, experiment_name: str) -> None:
        """
        Initialize the Vertex AI Tensorboard Logger.

        Args:
            log_dir (str): Directory where logs will be stored.
            experiment_name (str): Name of the experiment in Vertex AI.
        """
        self.log_dir = log_dir
        self.experiment_name = experiment_name
        self.tensorboard_id = os.getenv("SMLP_TENSORBOARD_ID")

    def ensure_log_dir_exists(self) -> None:
        """
        Ensure that the log directory exists, creating it if necessary.

        Returns:
            None
        """
        os.makedirs(self.log_dir, exist_ok=True)

    def stream_tensorboard_logs(self) -> None:
        """
        Start real-time streaming of logs to Vertex AI TensorBoard.

        Returns:
            None
        """
        self.ensure_log_dir_exists()
        aiplatform.start_upload_tb_log(
            tensorboard_id=self.tensorboard_id,
            tensorboard_experiment_name=self.experiment_name,
            logdir=self.log_dir,
        )

    def upload_tensorboard_logs(self) -> None:
        """
        Perform a one-time upload of logs to Vertex AI TensorBoard.

        Returns:
            None
        """
        self.ensure_log_dir_exists()
        aiplatform.upload_tb_log(
            tensorboard_id=self.tensorboard_id,
            tensorboard_experiment_name=self.experiment_name,
            logdir=self.log_dir,
        )

    def stop_logging(self) -> None:
        """
        Stop real-time logging to Vertex AI TensorBoard.

        Returns:
            None
        """
        aiplatform.end_upload_tb_log()