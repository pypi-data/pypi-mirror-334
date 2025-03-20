from abc import ABC, abstractmethod
from typing import Dict, Any

class Logger(ABC):
    """
    Abstract Factory Interface for creating loggers.
    """
    @abstractmethod
    def vertex_experiment_logger(self) -> 'ExperimentLogger':
        """
        Create an ExperimentLogger.

        Returns:
            ExperimentLogger: The created ExperimentLogger.
        """
        pass
    
    @abstractmethod
    def vertex_tensorboard_logger(self, log_dir: str) -> 'TensorboardLogger':
        """
        Create a TensorboardLogger.

        Args:
            log_dir (str): Directory where logs will be stored.

        Returns:
            TensorboardLogger: The created TensorboardLogger.
        """
        pass

class ExperimentLogger(ABC):
    """
    Abstract Product Interface for Experiment Logger.
    """
    @abstractmethod
    def start_run(self, run_name: str, existing_run: bool = False) -> None:
        """
        Start a new run in the experiment.

        Args:
            run_name (str): Name of the run.
            existing_run (bool): Whether to resume an existing run.

        Returns:
            None
        """
        pass

    @abstractmethod
    def log_metrics(self, metrics: Dict[str, float], step: int) -> None:
        """
        Log metrics to the experiment.

        Args:
            metrics (Dict[str, float]): Dictionary containing metrics.
            step (int): Training step.

        Returns:
            None
        """
        pass
    
    @abstractmethod
    def log_params(self, params: Dict[str, Any]) -> None:
        """
        Log hyperparameters to the experiment.

        Args:
            params (Dict[str, Any]): Dictionary containing hyperparameters.

        Returns:
            None
        """
        pass
    
    @abstractmethod
    def end_run(self) -> None:
        """
        End the current run in the experiment.

        Returns:
            None
        """
        pass

class TensorboardLogger(ABC):
    """
    Abstract Product Interface for Tensorboard Logger.
    """
    @abstractmethod
    def stream_tensorboard_logs(self) -> None:
        """
        Start real-time streaming of logs to TensorBoard.

        Returns:
            None
        """
        pass

    @abstractmethod
    def upload_tensorboard_logs(self) -> None:
        """
        Perform a one-time upload of logs to TensorBoard.

        Returns:
            None
        """
        pass

    @abstractmethod
    def stop_logging(self) -> None:
        """
        Stop real-time logging to TensorBoard.

        Returns:
            None
        """
        pass