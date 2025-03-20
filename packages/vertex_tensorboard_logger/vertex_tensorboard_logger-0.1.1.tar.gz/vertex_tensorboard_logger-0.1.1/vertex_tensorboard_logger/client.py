import time
import shutil

import tensorflow as tf

from .interface import Logger
from .factory import VertexAILogger

def run_experiment(factory: Logger) -> None:
    """
    Run an experiment using the provided logger factory.

    Args:
        factory (Logger): The logger factory to use for creating loggers.

    Returns:
        None
    """
    experiment_logger = factory.vertex_experiment_logger()
    experiment_logger.start_run("test-run-4")
    
    # Log Parameters
    experiment_logger.log_params({"learning_rate": 0.01, "batch_size": 32})

    # Simulate Training Steps
    for step in range(5):
        time.sleep(1)  # Simulate computation time
        experiment_logger.log_time_series_metrics({"accuracy": 0.9 + step * 0.01}, step)
    experiment_logger.end_run()

    tb_logger = factory.vertex_tensorboard_logger("./logs")
    # Start Streaming Logs
    tb_logger.stream_tensorboard_logs()
    try:
        (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
        x_train, x_test = x_train / 255.0, x_test / 255.0

        def create_model() -> tf.keras.models.Sequential:
            """
            Create a simple neural network model.

            Returns:
                tf.keras.models.Sequential: The created model.
            """
            return tf.keras.models.Sequential(
                [
                    tf.keras.layers.Flatten(input_shape=(28, 28)),
                    tf.keras.layers.Dense(512, activation="relu"),
                ]
            )

        model = create_model()
        model.compile(
            optimizer="adam",
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"]
        )

        tensorboard_callback = tf.keras.callbacks.TensorBoard(
            log_dir="test_log_dir",
            histogram_freq=1
        )

        model.fit(
            x=x_train,
            y=y_train,
            epochs=5,
            validation_data=(x_test, y_test),
            callbacks=[tensorboard_callback],
        )

    finally:
        tb_logger.stop_logging()
        
    shutil.rmtree("test_log_dir")

if __name__ == "__main__":
    vertex_ai_factory = VertexAILogger("test-logging-gk-experiment")
    run_experiment(vertex_ai_factory)