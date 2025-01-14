import tensorflow as tf
import numpy as np
import os


class MainManager:
    def __init__(self):
        """
        Initialize the MainManager by loading the MK1.h5 model.
        Sets up the 'brain' attribute that will be used for predictions.
        """
        try:
            # Build path to Save folder (one level up)
            save_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Save')
            model_path = os.path.join(save_dir, 'MK1.h5')

            # Load the model
            self.brain = tf.keras.models.load_model(model_path)
            print(f"Model successfully loaded from: {model_path}")

        except Exception as e:
            print(f"Error loading model: {str(e)}")
            self.brain = None
            raise Exception("Failed to initialize MainManager: Model could not be loaded")

    def compute(self, image):
        """
        Compute predictions for a given image.

        Parameters:
        image: numpy array of shape (28, 28) or (28, 28, 1)

        Returns:
        numpy array of shape (10,) containing probabilities for each digit (0-9)
        """
        if self.brain is None:
            raise Exception("Model not properly loaded")

        # Handle different input shapes
        if image.shape == (28, 28):
            processed_image = image.reshape(1, 28, 28, 1)
        elif image.shape == (28, 28, 1):
            processed_image = image.reshape(1, 28, 28, 1)
        else:
            raise ValueError("Image must be 28x28 pixels")

        # Normalize if not already done
        if processed_image.max() > 1:
            processed_image = processed_image.astype('float32') / 255

        # Get predictions
        predictions = self.brain.predict(processed_image, verbose=0)

        # Return the probability array for each digit
        return predictions[0]  # Return the first (and only) prediction array


#DEBUG STUFF TO BE DELETED BEFORE RELEASE
""""
# Example usage
if __name__ == "__main__":
    # Create manager instance
    manager = MainManager()

    # Load a test image for demonstration
    (_, _), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
    test_image = x_test[0]  # Take first test image

    # Get predictions
    probabilities = manager.compute(test_image)

    # Print results
    print("\nPrediction probabilities for each digit:")
    for digit, probability in enumerate(probabilities):
        print(f"Digit {digit}: {probability * 100:.2f}%")

    print(f"\nPredicted digit: {np.argmax(probabilities)}")
    print(f"True digit: {y_test[0]}")

"""