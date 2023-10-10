import cv2

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(-1)

while True:
    ret, frame = video_capture.read() # return code and frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale( #experiment with different numbers in here
        gray,
        scaleFactor=1.1, # adjusts for further away and back
        # detection algorithm uses a window to search, minsize is the size of the window
        # minNeighbours gives how many things need to be detected to declare a face
        minNeighbors=5,
        minSize=(30, 30),
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done release the camera and destroy any open windows
video_capture.release()
cv2.destroyAllWindows()