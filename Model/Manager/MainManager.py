import tensorflow as tf
import numpy as np
import os


class MainManager:
    def __init__(self):
        try:
            save_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Save')
            model_path = os.path.join(save_dir, 'MK1.h5')

            self.brain = tf.keras.models.load_model(model_path)
            print(f"Model successfully loaded from: {model_path}")

        except Exception as e:
            print(f"Error loading model: {str(e)}")
            self.brain = None
            raise Exception("Failed to initialize MainManager: Model could not be loaded")

    def compute(self, grid):
        image = self.parse_into_image(grid)
        if self.brain is None:
            raise Exception("Model not properly loaded")

        if image.shape == (28, 28):
            processed_image = image.reshape(1, 28, 28, 1)
        elif image.shape == (28, 28, 1):
            processed_image = image.reshape(1, 28, 28, 1)

        if processed_image.max() > 1:
            processed_image = processed_image.astype('float32') / 255

        predictions = self.brain.predict(processed_image, verbose=0)
        rounded_predictions = np.round(predictions[0] * 100, 3)  # Multiply by 100 and round to the nearest hundredth
        return rounded_predictions
    def parse_into_image(self, grid):
        return np.expand_dims(grid, axis=-1)
