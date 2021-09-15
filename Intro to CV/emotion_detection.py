import cv2
from fer import FER
import time
# import matplotlib.pyplot as plt


# # Get a reference to webcam
# video_capture = cv2.VideoCapture(0)
#
# emotion_dict = {
#     0: 'Surprise',
#     1: 'Happy',
#     2: 'Disgust',
#     3: 'Anger',
#     4: 'Sadness',
#     5: 'Fear',
#     6: 'Contempt'
# }
#

def face_detection():
    # Load the cascade
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # To capture video from webcam.
    cap = cv2.VideoCapture(0)
    # To use a video file as input
    # cap = cv2.VideoCapture('filename.mp4')

    while True:
        # Read the frame
        _, img = cap.read()
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect the faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 3)
        # Draw the rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        # Display
        cv2.imshow('img', img)
        # Stop if escape key is pressed
        k = cv2.waitKey(30) & 0xff
        if k==27:
            break
    # Release the VideoCapture object
    cap.release()


def emotion_fer():
    detector = FER(mtcnn=True)
    cap = cv2.VideoCapture(0)

    while True:
        # Read the frame
        _, img = cap.read()
        # Convert to grayscale
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect the faces
        # detector = FER(mtcnn=True)
        detected = detector.detect_emotions(img)
        print(detected)

        for face in detected:
            detected_emotions = face['emotions']
            print(detected_emotions)

            # Find the strongest emotion
            top_emotion = 'neutral'
            for emotion in detected_emotions:
                if detected_emotions[emotion] > detected_emotions[top_emotion]:
                    top_emotion = emotion

            # Get the coordinates of the box that contains the face
            (x, y, w, h) = face['box']

            # Add the strongest emotion to the image
            img = cv2.putText(img=img, text=f"{top_emotion}", org=(x, y), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                              fontScale=1, color=(255, 0, 0), thickness=2, lineType=cv2.LINE_AA)

            # Add a blue box around the detected face
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Display
        cv2.imshow(winname='Feeling Detection', mat=img)

        # Stop if escape key is pressed
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
        # Release the VideoCapture object
    cap.release()

emotion_fer()
