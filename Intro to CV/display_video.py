import numpy as np
import cv2 as cv


def video_from_camera():
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # Our operations on the frame come here
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # Display the resulting frame only for one millisecond
        # Press 'q' to stop the video stream
        cv.imshow('frame', gray)
        if cv.waitKey(1) == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()


def video_from_file(name):
    cap = cv.VideoCapture(f"{name}.avi")
    while cap.isOpened():
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # Rotate the frame: 0 = 90 degree, 1 = 180 degree, 2 = 270 degree
        # frame = cv.rotate(frame, 3)

        # Vertical flip to the video
        # frame = cv.flip(frame, 0)

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        cv.imshow('frame', gray)
        if cv.waitKey(25) == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()


def save_video_from_camrea(name):
    cap = cv.VideoCapture(0)

    # Define the codec and create VideoWriter object
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    # 20.0 is the fps??
    out = cv.VideoWriter(f"{name}.avi", fourcc, 20.0, (640, 480))
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # write the frame
        out.write(frame)
        cv.imshow('frame', frame)
        if cv.waitKey(1) == ord('q'):
            break
    # Release everything if job is finished
    cap.release()
    out.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    # save_video_from_camrea(name='library_view')
    video_from_file(name='library_view')
