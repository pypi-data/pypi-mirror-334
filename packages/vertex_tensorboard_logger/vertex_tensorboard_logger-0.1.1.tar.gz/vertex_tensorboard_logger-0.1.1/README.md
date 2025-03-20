# Vertex AI Logger

Logger for monitoring and visualizing machine learning training processes within Vertex AI.

## Installation
```pip install vertex_tensorboard_logger```

## Setup

1. Authenticate with Google Cloud:
```bash
gcloud auth application-default login
```

2. Set Environment Variables:

 Set the necessary environment variables for your Google Cloud project:

3. Add GCP Secrets to Access Google cloud projects: 


## Usage

1. Initialize the Logger:
```python
from vertex_tensorboard_logger import VertexAILogger

factory = VertexAILogger(
    experiment_name="your_experiment_name"
)
```

2. Start a Experiment Run:
```python
experiment_logger = factory.vertex_experiment_logger()
experiment_logger.start_run(run_name="your_run_name", existing_run=False)
```

3. Log Metrics, Parameters, and Time Series Data:
```python
# Log metrics
metrics = {"accuracy": 0.95}
experiment_logger.log_metrics(metrics)

# Log hyperparameters
params = {"learning_rate": 0.001, "num_train_epochs": 3, "warmup_ratio": 0.1, "weight_decay": 0.01}
experiment_logger.log_params(params)

# Log time series metrics
time_series_metrics = {"accuracy": 0.95, "F1-score": 0.85}
experiment_logger.log_time_series_metrics(time_series_metrics, step=1)
```

4. End the Experiment Run:
```python
experiment_logger.end_run()
```

5. Stream TensorBoard Logs:
```python
tensorboard_logger = factory.vertex_tensorboard_logger(log_dir="path_to_log_directory")
tensorboard_logger.stream_tensorboard_logs()
# Training Code
tensorboard_logger.stop_logging()
```

6. Upload TensorBoard Logs:
```python
tensorboard_logger.upload_tensorboard_logs()
```