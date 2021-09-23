import numpy as np
from scipy import misc
import matplotlib.pyplot as plt

# Convolution is the treatment of a matrix by another one which is called “kernel”.
# The first matrix (bi-dimensional image) is multiplied by a 3X3 or 5x5 matrix (the kernel).
# The kernel "iterates" over each pixel, and filters/transforms it to a new value
# this practice can be used to enhance feature extraction, edge detection, blur, sharpen, etc.

# A little about filters
# This filter detects edges nicely
# It creates a filter that only passes through sharp edges and straight lines.
# Experiment with different values for fun effects.
# filter = [ [0, 1, 0], [1, -4, 1], [0, 1, 0]]
# A couple more filters to try for fun!
# filter = [ [-1, -2, -1], [0, 0, 0], [1, 2, 1]]
# filter = [ [-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
# If all the digits in the filter don't add up to 0 or 1, you
# should probably do a weight to get it to do so
# so, for example, if your weights are 1,1,1 1,2,1 1,1,1
# They add up to 10, so you would set a weight of .1 if you want to normalize them

stairs_img = misc.ascent()
image_transformed = np.copy(stairs_img)
size_x = image_transformed.shape[0]
size_y = image_transformed.shape[1]

filter = [[-1, -2, -1],
          [0, 0, 0],
          [1, 2, 1]]
weight = 1

for x in range(1,size_x-1):
    for y in range(1, size_y-1):
        output_pixel = 0.0
        # Update each pixel in the image by multiplying its the surrounding 3x3 square with the kernel
        for row in range(3):
            for col in range(3):
                output_pixel = output_pixel + (stairs_img[x + col - 1, y + row - 1] * filter[row][col])

        output_pixel = output_pixel * weight
        if output_pixel < 0:
            output_pixel = 0
        if output_pixel > 255:
            output_pixel = 255
        image_transformed[x, y] = output_pixel

# At this point, the transformed image's size is the same as the original one.
# One of the goals of using convolutions is to save us time.
# After detecting the features of the image, we can create a new image which is smaller and has the main features of the image
# This is called pooling.
# The following code will show a (2, 2) pooling called Max Pooling, since it takes the Max between the four pixels.
# As a result we'll end up having an image with 1/4 of the original size.

new_x = int(size_x/2)
new_y = int(size_y/2)
newImage = np.zeros((new_x, new_y))
for x in range(0, size_x, 2):
    for y in range(0, size_y, 2):
        pixels = []
        pixels.append(image_transformed[x, y])
        pixels.append(image_transformed[x+1, y])
        pixels.append(image_transformed[x, y+1])
        pixels.append(image_transformed[x+1, y+1])
        pixels.sort(reverse=True)
        newImage[int(x/2),int(y/2)] = pixels[0]

plt.grid(False)
plt.gray()
plt.axis('on')
plt.imshow(newImage)
plt.show()
