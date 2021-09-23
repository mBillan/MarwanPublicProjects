import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# The module is on this tutorial
# https://developers.google.com/codelabs/tensorflow-4-cnns#3


# Load the fashion minst collection from tf.keras
mnist = tf.keras.datasets.fashion_mnist

# load the training and testing data
(training_images, training_labels),  (test_images, test_labels) = mnist.load_data()

# Reshape the 60,000 training images to into a 4D list
training_images=training_images.reshape(60000, 28, 28, 1)
# Reshape the160,000 test images to into a 4D lis
test_images = test_images.reshape(10000, 28, 28, 1)

# Normalize the values to be 0-->1 rather than 0-->255
training_images = training_images/255.0
test_images = test_images/255.0

# Define the model and the layers (units) in the neural network
model = tf.keras.models.Sequential([
    # A layer of 64 different 3x3 convolutions
    tf.keras.layers.Conv2D(filters=64, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)),
    tf.keras.layers.MaxPooling2D(2, 2),

    # Another layer of convolutions adds a layer of sub-features
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),

    # Now continue as the basic detector
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Shows the shape of the output in each layer,
model.summary()

# Train the model based on the given training sets.
model.fit(training_images, training_labels, epochs=5)
test_loss, test_accuracy = model.evaluate(test_images, test_labels)
print('Test loss: {}, Test accuracy: {}'.format(test_loss, test_accuracy*100))


# Returns a list of classification.
# each element is also a list of the probability that the image is each one of the categories
classifications = model.predict(test_images)

img_number = 10
print(classifications[img_number])
# [1.0548181e-05 1.3723358e-08 6.3520893e-06 2.7897144e-08 3.4400477e-06
#  1.5837485e-02 4.1048192e-05 8.8573523e-02 8.0439153e-05 8.9544708e-01]
print(f"The closest category is: {np.argmax(classifications[img_number])}")

print(f"The test original label is: {test_labels[img_number]}")

plt.grid(False)
plt.gray()
plt.axis('on')
plt.imshow(test_images[img_number])
plt.show()
