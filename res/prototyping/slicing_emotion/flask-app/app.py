from flask import Flask, render_template, request, redirect
from flask_sock import Sock
import base64
import cv2
import numpy as np
import urllib
from keras.models import load_model
import json
import os

app = Flask(__name__)
sock = Sock(app)

frontfaceCascPath = "./models/haarcascade_frontalface_default.xml"
sidefaceCascPath = "./models/haarcascade_profileface.xml"
eyeCascPath = "./models/haarcascade_eye.xml"

faceCascade = cv2.CascadeClassifier(frontfaceCascPath)
profileCascade = cv2.CascadeClassifier(sidefaceCascPath)
eyeCascade = cv2.CascadeClassifier(eyeCascPath)


# given an image, detects faces, draws boxes around them and then crops out img for each face
# returns an array of paths for the individual faces
def face_detect(path):  
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #change to grayscale

    faces = faceCascade.detectMultiScale( #experiment with different numbers in here
        gray,
        scaleFactor=1.05, # the closer to one, the slower but better, away from 1 is faster but less accurate
        minNeighbors=5, 
        minSize=(20, 20), # smallest size object that can be detected, i.e. for eyes we need smaller as they are smaller, maybe reduce this to get faces further away
    )

    profiles = profileCascade.detectMultiScale(
        gray,
        scaleFactor = 1.05,
        minNeighbors=5,
        minSize=(20,20),
    )

    i = 0
    faces_array = []
    for (x, y, w, h) in faces: # draw rectangles around faces
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

        crop_path = "faces/crop_face" + str(i) + ".png"

        crop = img[y:y+h, x:x+w].copy()
        cv2.imwrite(crop_path, crop)
        faces_array.append(crop_path)
        i += 1

    front_faces = len(faces)
    
    for (x,y,w,h) in profiles:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255,0,0), 2)

        crop_path = "faces/crop_face" + str(i) + ".png"

        crop = img[y:y+h, x:x+w].copy()
        cv2.imwrite(crop_path, crop)
        faces_array.append(crop_path)
        i += 1

    profile_faces = len(profiles)
        
    # faces is an array of arrays, each face is an array of four points, x, y, w, h
    # x, y is top left of box, x+w, y+h is bottom right of box
    # rectangle uses (image to draw on, start point, end point, color, thickness)

    path = 'image_after.png'
    cv2.imwrite(path, img)

    return faces_array, front_faces, profile_faces

# given an array of image paths, goes through each one, resizes them and runs predict_emotion on each, returns array of detected emotion
def check_emotions(array):
    emotions = []
    for img in array:
        try:
            face_image = cv2.imread(img)
            face_image = cv2.resize(face_image, (48,48))
            face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
            face_image = np.reshape(face_image, [1, face_image.shape[0], face_image.shape[1], 1])

            label = predict_emotion(face_image)
            emotions.append(label)
        except Exception as e:
            print(str(e))
    return emotions
        
def predict_emotion(image):
    emotion_dict= {'Angry': 0, 'Sad': 5, 'Neutral': 4, 'Disgust': 1, 'Surprise': 6, 'Fear': 2, 'Happy': 3}
    model = load_model("./models/model_v6_23.hdf5")

    predicted_class = np.argmax(model.predict(image))
    label_map = dict((v,k) for k,v in emotion_dict.items()) 
    predicted_label = label_map[predicted_class]
    return predicted_label

def detect_eyes(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #change to grayscale

    eyes = eyeCascade.detectMultiScale( #experiment with different numbers in here
        gray,
        scaleFactor=1.1, # adjusts for further away and back
        minNeighbors=10,
        minSize=(10, 10),
    )

    for (x, y, w, h) in eyes: # draw rectangles around eyes
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 255), 2)

    cv2.imwrite(path, img)

    return len(eyes)

# converts a local image to a data URL that can be sent via sockets
def image_to_data_url(filepath): 
    ext = filepath.split('.')[-1]
    prefix = f'data:image/{ext};base64,'
    with open(filepath, 'rb') as f:
        img = f.read()
    return prefix + base64.b64encode(img).decode('utf-8')

### App Routes

@app.route('/')
def index():
    return render_template('index.html')

### Socket Route

@sock.route('/identify')
def identify(sock):
    img_path = 'image_before.png'
    while True:
        data = sock.receive() # data comes in as a data uri

        response = urllib.request.urlopen(data)
        with open(img_path, 'wb') as f:
            f.write(response.file.read())

        faces_array, front_faces, profile_faces = face_detect(img_path)
        return_url = image_to_data_url("image_after.png")
        emotion_array = check_emotions(faces_array)
        
        small_pic_urls = []
        for face in faces_array:
            num_eyes = detect_eyes(face)
            url = image_to_data_url(face)
            small_pic_urls.append(url)
    
        # return url is the data url of the big picture, showing faces detected
        # faces array is image paths, pointing to each cropped face image, they have eyes on them after going through eye detection
        # emotion array is a list is a list of strings, emotions detected in each face

        # I want to return an array of three things [1. big picture to display, 2. small pics to display, 3. emotions detected]
        # [return_url, small_pic_urls, emotion_array]

        return_json = {
            "picture" : return_url,
            "urls" : small_pic_urls,
            "emotions" : emotion_array,
            "eyes" : num_eyes,
            "faces" : front_faces,
            "profiles" : profile_faces
        }

        data = json.dumps(return_json)

        sock.send(data)

        os.remove("image_after.png")
        os.remove("image_before.png")
        os.chdir("faces")
        files = os.listdir()
        for file in files:
            os.remove(file)
        os.chdir("..")

if __name__ == "__main__":
    app.run(debug=False)