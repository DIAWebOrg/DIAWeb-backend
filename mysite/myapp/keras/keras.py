import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Input

# Load the MNIST dataset
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Normalize the pixel values to the range [0, 1]
x_train, x_test = x_train / 255.0, x_test / 255.0

# Define your Keras model
def create_model():
    model = Sequential([
        Input(shape=(28, 28)),  
        Flatten(),
        Dense(128, activation='relu'),
        Dense(10, activation='softmax')
    ])
    return model

# Detect if TPU is available
try:
    resolver = tf.distribute.cluster_resolver.TPUClusterResolver()  # TPU detection
    tf.config.experimental_connect_to_cluster(resolver)
    tf.tpu.experimental.initialize_tpu_system(resolver)
    strategy = tf.distribute.TPUStrategy(resolver)
    print('Running on TPU')
except ValueError:
    # If TPU not available, fallback to GPU or CPU
    strategy = tf.distribute.MirroredStrategy()  # This works for single-GPU or multi-GPU setups
    print('Running on GPU' if tf.config.list_physical_devices('GPU') else 'Running on CPU')

# Create and compile the model inside the strategy scope
with strategy.scope():
    model = create_model()
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

# Train the model
model.fit(x_train, y_train, epochs=5, batch_size=128, validation_data=(x_test, y_test))

# Save the model
# model.save("model.keras")