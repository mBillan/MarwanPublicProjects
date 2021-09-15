import numpy as np
import cv2 as cv

start_time = cv.getTickCount()

# Create a black image
square_size = 512
img = np.zeros((square_size, square_size, 3), np.uint8)

# Draw a diagonal green line with thickness of 5 px
rgb_color = (0, 255, 0)  # (blue, green, red)
thickness = 5
point_1 = (0, 0)
point_2 = (square_size//2, square_size//2)
cv.line(img, point_1, point_2, color=rgb_color, thickness=thickness)

point_3 = (square_size-1, 0)
cv.line(img, point_2, point_3, color=rgb_color, thickness=thickness)

top_left = (384, 0)
bottom_right = (510, 128)
rgb_color = (255, 0, 0)
cv.rectangle(img, top_left , bottom_right, rgb_color, 3)

# Draw a circle inside the rectangle
center = (447, 63)
radius = 63
rgb_color = (0, 230, 255)
cv.circle(img, center, radius, rgb_color, -1)

cv.ellipse(img, (256, 256), (100, 50), 0, 0, 180, 255, -1)

pts = np.array([[10, 5], [20, 30], [70, 20], [50, 10]], np.int32)
pts = pts.reshape((-1, 1, 2))
cv.polylines(img, [pts], True, (0, 255, 255))

cv.imshow("Display window", img)
cv.waitKey(0)


end_time = cv.getTickCount()
time = (end_time - start_time)/ cv.getTickFrequency()
print(f"This program took {time} seconds to complete")