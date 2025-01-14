import tensorflow as tf
import numpy as np
from tensorflow.keras import models, layers
import os


def train_mnist_model():
    # Build path to Save folder (one level up)
    save_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Save')

    # Create Save folder if it doesn't exist
    if not os.path.exists(save_dir):
        try:
            os.makedirs(save_dir)
            print(f"Save folder created: {save_dir}")
        except Exception as e:
            print(f"Error creating Save folder: {str(e)}")
            return None, None

    # Ask user for filename
    model_name = input("Enter name to save your model: ")

    # Add .h5 extension if not present
    if not model_name.endswith('.h5'):
        model_name += '.h5'

    # Build complete file path
    model_path = os.path.join(save_dir, model_name)

    print(f"\nModel will be saved as: {model_path}")
    print("\nLoading data...")

    # 1. Load and prepare data
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

    # Normalize pixels between 0 and 1
    x_train = x_train.astype('float32') / 255
    x_test = x_test.astype('float32') / 255

    # Reshape to have correct input format (28x28x1)
    x_train = x_train.reshape((60000, 28, 28, 1))
    x_test = x_test.reshape((10000, 28, 28, 1))

    print("Creating model...")

    # 2. Create model
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(10, activation='softmax')
    ])

    # 3. Compile model
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    print("\nStarting training...")

    # 4. Train model with 10 epochs
    history = model.fit(
        x_train,
        y_train,
        epochs=10,
        batch_size=64,
        validation_split=0.2,
        verbose=1
    )

    # 5. Evaluate on test set
    test_loss, test_acc = model.evaluate(x_test, y_test)
    print(f"\nFinal accuracy on test set: {test_acc:.4f}")

    # 6. Save model
    try:
        model.save(model_path)
        print(f"\nModel successfully saved at: {model_path}")
    except Exception as e:
        print(f"\nError while saving model: {str(e)}")

    return history, model


if __name__ == "__main__":
    print("Welcome to MNIST model training!")
    history, model = train_mnist_model()