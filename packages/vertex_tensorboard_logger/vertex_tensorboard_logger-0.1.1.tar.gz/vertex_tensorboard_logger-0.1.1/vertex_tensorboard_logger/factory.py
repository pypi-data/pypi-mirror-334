from typing import Dict, Any

from .interface import Logger, ExperimentLogger, TensorboardLogger
from .product import VertexAIExperimentLogger, VertexAITensorboardLogger

class VertexAILogger(Logger):
    """
    Concrete Factory for creating Vertex AI loggers.
    """
    def __init__(self, experiment_name: str) -> None:
        """
        Initialize the Vertex AI Logger Factory.

        Args:
            experiment_name (str): Name of the experiment in Vertex AI.
        """
        self.experiment_name: str = experiment_name

    def vertex_experiment_logger(self) -> 'ExperimentLogger':
        """
        Create a Vertex AI Experiment Logger.

        Returns:
            ExperimentLogger: The created Vertex AI Experiment Logger.
        """
        return VertexAIExperimentLogger(self.experiment_name)
    
    def vertex_tensorboard_logger(self, log_dir: str) -> 'TensorboardLogger':
        """
        Create a Vertex AI Tensorboard Logger.

        Args:
            log_dir (str): Directory where logs will be stored.

        Returns:
            TensorboardLogger: The created Vertex AI Tensorboard Logger.
        """
        return VertexAITensorboardLogger(log_dir, self.experiment_name)




