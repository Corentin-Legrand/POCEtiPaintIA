import tensorflow as tf
import numpy as np
import os


class MainManager:
    def __init__(self):
        """
        Initialize the MainManager by loading the MK1.h5 model.
        Configures GPU memory usage and sets up the model.
        """
        # GPU Configuration
        self._setup_gpu()

        try:
            save_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Save')
            model_path = os.path.join(save_dir, 'MK1.h5')

            self.brain = tf.keras.models.load_model(model_path)
            print(f"Model successfully loaded from: {model_path}")

            # Move model to GPU if available
            if len(tf.config.list_physical_devices('GPU')) > 0:
                print("Model running on GPU")
            else:
                print("WARNING: No GPU found, running on CPU")

        except Exception as e:
            print(f"Error loading model: {str(e)}")
            self.brain = None
            raise Exception("Failed to initialize MainManager: Model could not be loaded")

    def _setup_gpu(self):
        """
        Configure GPU settings for optimal performance
        """
        try:
            gpus = tf.config.list_physical_devices('GPU')

            if gpus:
                for gpu in gpus:
                    # Configure memory growth
                    tf.config.experimental.set_memory_growth(gpu, True)

                print(f"Found {len(gpus)} GPU(s):")
                for gpu in gpus:
                    print(f"- {gpu.device_type}: {gpu.name}")
            else:
                print("No GPU devices found")

        except RuntimeError as e:
            print(f"GPU configuration error: {str(e)}")

    def compute(self, grid):
        """
        Compute predictions for a given grid using GPU acceleration.

        Parameters:
        grid: numpy array representing the input grid

        Returns:
        numpy array of rounded predictions (percentages)
        """
        image = self.parse_into_image(grid)
        if self.brain is None:
            raise Exception("Model not properly loaded")

        if image.shape == (28, 28):
            processed_image = image.reshape(1, 28, 28, 1)
        elif image.shape == (28, 28, 1):
            processed_image = image.reshape(1, 28, 28, 1)

        if processed_image.max() > 1:
            processed_image = processed_image.astype('float32') / 255

        # Convert to TensorFlow tensor
        tensor_image = tf.convert_to_tensor(processed_image, dtype=tf.float32)

        # Get predictions using GPU if available
        with tf.device('/GPU:0' if len(tf.config.list_physical_devices('GPU')) > 0 else '/CPU:0'):
            predictions = self.brain.predict(tensor_image, verbose=0)

        rounded_predictions = np.round(predictions[0] * 100, 3)  # Multiply by 100 and round to the nearest thousandth
        return rounded_predictions

    def parse_into_image(self, grid):
        """
        Parse grid into image format
        """
        return np.expand_dims(grid, axis=-1)

    def get_device_info(self):
        """
        Returns information about the devices being used
        """
        devices_info = {
            "GPUs": [],
            "Current_device": "CPU"
        }

        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            devices_info["GPUs"] = [gpu.name for gpu in gpus]
            devices_info["Current_device"] = "GPU"

        return devices_info