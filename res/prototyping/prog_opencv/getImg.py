import cv2
import sys
import time

imagePath = sys.argv[1]

image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cascPath = "haarcascade_frontalface_default.xml"

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)


# Detect faces in the image
faces = faceCascade.detectMultiScale(gray, scaleFactor=1.4, minNeighbors=5, minSize=(30, 30))

print("Found {0} faces!".format(len(faces)))

# Draw a rectangle around the faces
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

cv2.imshow("Faces Found", image)
cv2.waitKey(0)

cv2.imwrite("ChangedAbba.jpg", image)  
