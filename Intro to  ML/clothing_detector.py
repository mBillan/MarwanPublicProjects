import tensorflow as tf
import numpy as np

# The module is on this tutorial
# https://colab.research.google.com/github/lmoroney/mlday-tokyo/blob/master/Lab2-Computer-Vision.ipynb#scrollTo=dIn7S9gf62ie


# Load the fashion minst collection from tf.keras
mnist = tf.keras.datasets.fashion_mnist

# load the training and testing data
(training_images, training_labels),  (test_images, test_labels) = mnist.load_data()


# Normalize the values to be 0-->1 rather than 0-->255
training_images = training_images/255.0
test_images = test_images/255.0

# Define the model and the number of layer (units) in the neural network
# Each layer has a specific kind of function that tells the neuron how to analyze the data
# In this case
#     - The first layer Flattens the data (turns the squared image into one dimensional sequence)
#     - The second contains 128 neurons using the RELU functions (If X>0 return X, else return 0)
#     - The final layer contains 10 neurons of softmax which converts the number to probabilities.
#
# Note: the final layer usually should contain the same number of neurons as the categories we expect to have
#    In this example, for each input it would generate a list of 10 elements describing the probability of each category
model = tf.keras.models.Sequential([tf.keras.layers.Flatten(),
                                    tf.keras.layers.Dense(128, activation=tf.nn.relu),
                                    tf.keras.layers.Dense(10, activation=tf.nn.softmax)])

# Define how the model compiles the data.
# Meaning, how does it calculate the error (loss) and how to make it better (optimizer) in each iteration (epoch)
model.compile(optimizer=tf.keras.optimizers.Adam(),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Train the model based on the given training sets.
model.fit(training_images, training_labels, epochs=5)

model.evaluate(test_images, test_labels)

# Returns a list of classification.
# each element is also a list of the probability that the image is each one of the categories
classifications = model.predict(test_images)


print(classifications[0])
# [1.0548181e-05 1.3723358e-08 6.3520893e-06 2.7897144e-08 3.4400477e-06
#  1.5837485e-02 4.1048192e-05 8.8573523e-02 8.0439153e-05 8.9544708e-01]
print(f"The closest category is: {np.argmax(classifications[0])}")

print(f"The test original label is: {test_labels[0]}")
