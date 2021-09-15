import cv2 as cv
import sys


def read_img():
    # read an image
    img = cv.imread(cv.samples.findFile("starry_night.jpg"))

    if img is None:
        sys.exit("Could not read the image.")

    cv.imshow("Display window", img)

    # wait until the user presses any key and return the pressed key. (Zero means wait forever)
    k = cv.waitKey(0)

    # write the image as png if 's' was pressed
    if k == ord("s"):
        cv.imwrite("starry_night.png", img)


def arithmetic():
    img1 = cv.imread('m.png')
    img2 = cv.imread('opencv-logo.png')
    dst = cv.addWeighted(img1, 0.7, img2, 0.3, 0)
    cv.imshow('dst', dst)
    cv.waitKey(0)
    cv.destroyAllWindows()



def manipulating_img():
    img = cv.imread(cv.samples.findFile("missi.jpg"))

    if img is None:
        sys.exit("Could not read the image.")

    print(f"Getting pixel (100, 100)={img[100, 100]}")   # (blue, green, red)
    print(f"Getting pixel (100, 100) only the red ={img[100, 100, 2]}")

    # Assign a specific pixel with a specific value
    img[100, 100] = [255, 255, 255]
    print(f"Getting pixel (100, 100)={img[100, 100]}")   # (blue, green, red)

    # accessing RED value (better)
    print(img.item(100, 100, 2))
    img.itemset((100, 100, 2), 0)
    print(img.item(100, 100, 2))

    # size
    print(f"The shape of the image is:{img.shape}, size:{img.size} (px)")

    # Region of Interest
    head = img[50:110, 165:215]

    # copy it to another region
    img[:60, :50] = head

    # >> > b, g, r = cv.split(img)
    # >> > img = cv.merge((b, g, r))
    img[:, :, 2] = 0


    cv.imshow("Display window", img)
    # wait until the user presses any key and return the pressed key. (Zero means wait forever)
    k = cv.waitKey(0)
    if k == ord("s"):
        cv.imwrite("messi1_2.png", img)
manipulating_img()