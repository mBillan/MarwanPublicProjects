import numpy as np
import cv2 as cv

# events = [i for i in dir(cv) if 'EVENT' in i]
# print( events )


# def circle_on_click():
#     # mouse callback function
#     def draw_circle(event, x, y, flags, param):
#         if event == cv.EVENT_LBUTTONDBLCLK:
#             cv.circle(img, (x, y), 100, (255, 0, 0), -1)
#
#     # Create a black image, a window and bind the function to window
#     img = np.zeros((512, 512, 3), np.uint8)
#     cv.namedWindow('image')
#     cv.setMouseCallback('image', draw_circle)
#     while True:
#         cv.imshow('image', img)
#         # click ESC to exit
#         if cv.waitKey(20) & 0xFF == 27:
#             break
#     cv.destroyAllWindows()


drawing = False  # true if mouse is pressed
mode = True  # if True, draw rectangle. Press 'm' to toggle to curve
ix, iy = -1, -1


# mouse callback function
def draw_circle(event, x, y, flags, param):
    global ix, iy, drawing, mode, img
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv.EVENT_MOUSEMOVE:
        if drawing:
            if mode:
                img = np.zeros((512, 512, 3), np.uint8)

                cv.rectangle(img, (ix, iy), (x, y), (0, 255, 0), -1)
            else:
                cv.circle(img, (x, y), 5, (0, 0, 255), -1)
    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        if mode:
            cv.rectangle(img, (ix, iy), (x, y), (0, 255, 0), -1)
        else:
            cv.circle(img, (x, y), 5, (0, 0, 255), -1)


img = np.zeros((512, 512, 3), np.uint8)
cv.namedWindow('image')
cv.setMouseCallback('image', draw_circle)
while True:
    cv.imshow('image', img)
    k = cv.waitKey(1) & 0xFF
    if k == ord('m'):
        mode = not mode
    elif k == 27:
        break
cv.destroyAllWindows()
