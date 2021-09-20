import tensorflow as tf
import numpy as np
from tensorflow import keras

# The module is on this tutorial
# https://developers.google.com/codelabs/tensorflow-1-helloworld

# Define the model and the number of layer (units) in the neural network
model = tf.keras.Sequential([keras.layers.Dense(units=1, input_shape=[1])])


# Define how the model compiles the data.
# Meaning, how does it calculate the error (loss) and how to make it better (optimizer) in each iteration (epoch)
# sgd - stochastic gradient descent
model.compile(optimizer='sgd', loss='mean_squared_error')

# Subset from the Natural number
xs = np.array([-1.0, 0.0, 1.0, 2.0, 3.0, 4.0], dtype=float)
# Subset based on: y = 3x + 1
ys = np.array([-2.0, 1.0, 4.0, 7.0, 10.0, 13.0], dtype=float)

# Note: in ML the model tries to get as closer as possible to the correct solution but it might not hit it perfectly
# Train the model based on the given subsets.
# Try to find the closest relation from xs to ys in a specific number of iterations (epochs)
model.fit(xs, ys, epochs=500)
# Possible output:
# Epoch 500/500
# 1/1 [==============================] - 0s 999us/step - loss: 3.0600e-08

# Predict the Y of a given X
test_x = 10
print(f"Y({test_x}) = {model.predict([test_x])}")
# Possible output:
# Y(10) = [[30.999485]]
