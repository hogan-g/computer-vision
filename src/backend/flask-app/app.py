from flask import Flask, render_template, request, redirect
from flask_sock import Sock
import base64
import cv2
import urllib
import json
import os
import signal
import sys
import datetime
from deepface import DeepFace
import requests
import time

# when the flask is started it records what time it stats at
start_time = datetime.datetime.now()

# setup the flask app and socket
app = Flask(__name__)
sock = Sock(app)

# paths to our models
frontfaceCascPath = "./flask-app/models/haarcascade_frontalface_default.xml" 
sidefaceCascPath = "./flask-app/models/haarcascade_profileface.xml"
eyeCascPath = "./flask-app/models/haarcascade_eye.xml"

# load in our models into OpenCV
faceCascade = cv2.CascadeClassifier(frontfaceCascPath)
profileCascade = cv2.CascadeClassifier(sidefaceCascPath)
eyeCascade = cv2.CascadeClassifier(eyeCascPath)

# data taken in from command line when the subprocess is called
mcode = sys.argv[1]
lecture_id = sys.argv[2]
date = sys.argv[3]
time = sys.argv[4]
attendance = sys.argv[5]
day = sys.argv[6]

# this is the master dictionary, all data recorded during the session is stored in here
# will be stored in DB after session ends
data_captured = {
    "mcode" : mcode,
    "day" : day,
    "lecture_id" : lecture_id,
    "attendance" : attendance,
    "date" : date,
    "start_time" : time,
    "lecture_length" : "",
    "max_faces" : "",
    "min_faces" : "",
    "average_faces" : "",
    "faces_overtime" : "",
    "eyes_overtime" : "",
    "profiles_overtime" : "",
    "dominant_emotion" : "",
    "total_faces" : "",
    "total_eyes" : "",
    "total_profiles" : ""
}

# data constants
# each flask session/lecture these reset

total_faces = 0
max_faces = 0
min_faces = 100
emotion_list = []
capture_number = 0
faces_perCapture = []
eyes_perCapture = []
profiles_perCapture = []
total_eyes = 0
total_profiles = 0


# given an image, detects faces, draws boxes around them and then crops out img for each face
# returns an array of paths for the individual faces
def face_detect(path):  
    global capture_number
    global total_faces
    global total_profiles
    global max_faces
    global min_faces
    global faces_perCapture
    global profiles_perCapture
    
    # reads in our image into a cv2 format we can use
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #change to grayscale

    faces = faceCascade.detectMultiScale( #experiment with different numbers in here
        gray,
        # the closer to one, the slower but better, away from 1 is faster but less accurate
        scaleFactor=1.05, 
        minNeighbors=5, 
        minSize=(20, 20), 
        # smallest size object that can be detected, 
        # i.e. for eyes we need smaller as they are smaller, maybe reduce this to get faces further away
    )

    # same as detecting faces but uses the profile model and detects profiles 
    profiles = profileCascade.detectMultiScale(
        gray,
        scaleFactor = 1.05,
        minNeighbors=5,
        minSize=(20,20),
    )

    i = 0
    faces_array = []
    for (x, y, w, h) in faces: # draw rectangles around faces
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2) # make rectangle

        crop_path = "./flask-app/faces/crop_face" + str(i) + ".png" # generate path to crop image to

        crop = img[y-10:y+h+10, x-10:x+w+10].copy() # make a cropped image
        try:
            cv2.imwrite(crop_path, crop) # write the small cropped image to a file
            faces_array.append(crop_path) # record the file path so we can use it again
            i += 1
        except:
            pass

    front_faces = len(faces) ## the number of faces captured in one image
    faces_perCapture.append(front_faces)
    
    for (x,y,w,h) in profiles: # draw rectangle for profiles, the same as for faces
        cv2.rectangle(img, (x, y), (x+w, y+h), (255,0,0), 2)

        crop_path = "./flask-app/faces/crop_face" + str(i) + ".png"

        crop = img[y-10:y+h+10, x-10:x+w+10].copy()
        cv2.imwrite(crop_path, crop)
        faces_array.append(crop_path)
        i += 1

    profile_faces = len(profiles)
    profiles_perCapture.append(profile_faces)

        
    # faces is an array of arrays, each face is an array of four points, x, y, w, h
    # x, y is top left of box, x+w, y+h is bottom right of box
    # rectangle uses (image to draw on, start point, end point, color, thickness)

    path = 'image_after.png'
    cv2.imwrite(path, img) # store the image which has all the rectangles on it

    # data capture

    capture_number += 1 # increase the number of captures we have analyzed by one
    # add data to the dict
    total_faces += front_faces
    total_profiles += profile_faces
    
    if front_faces > max_faces:
        max_faces = front_faces
    if front_faces < min_faces:
        min_faces = front_faces

    return faces_array, front_faces, profile_faces, faces_perCapture

# given an array of image paths, goes through each one, resizes them and runs predict_emotion on each, returns array of detected emotion
def check_emotions(array):
    emotions = []
    for img in array:
        try:
            # try deepface analysis on the image
            face_analysis = DeepFace.analyze(img_path = img, enforce_detection=False, actions = ['emotion'])

            # add the resulting emotion to our list
            emotions.append(face_analysis[0]["dominant_emotion"])
        except: # if deepface can't run on the image, just pass it
            pass
    return emotions

# function to detect eyes in an image
def detect_eyes(path):
    global eyes_perCapture
    global total_eyes

    # use same method as faces but with the eye model

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

    eyes = len(eyes)
    total_eyes += eyes
    eyes_perCapture.append(eyes)

    return eyes

# converts a local image to a data URL that can be sent via sockets
def image_to_data_url(filepath): 
    ext = filepath.split('.')[-1]
    prefix = f'data:image/{ext};base64,'
    with open(filepath, 'rb') as f:
        img = f.read()
    return prefix + base64.b64encode(img).decode('utf-8')

# called at the end of the analysis to finalise the data packet
def prepare_data():
    # lecture length
    # record the end time so we can compare to start time
    end_time = datetime.datetime.now()

    data_captured["lecture_length"] = str(end_time - start_time)

    # emotion

    try:
        data_captured["dominant_emotion"] = max(set(emotion_list), key=emotion_list.count)
    except:
        pass
    # avg faces

    data_captured["average_faces"] = total_faces / capture_number

    data_captured["max_faces"] = max_faces
    data_captured["min_faces"] = min_faces

    data_captured["faces_overtime"] = faces_perCapture

    data_captured["eyes_overtime"] = eyes_perCapture
    data_captured["profiles_overtime"] = profiles_perCapture

    data_captured["total_faces"] = total_faces
    data_captured["total_profiles"] = total_profiles
    data_captured["total_eyes"] = total_eyes

    return data_captured

### App Routes
# the various routes that trigger our flask app to do things

# if the index is visited it shows the user our website
@app.route('/')
def index():
    return render_template('index.html')

# if /results is fetches the data is prepared and send to DB for storage
@app.route('/results')
def results():
    print("Results preparing to Send...")
    report_data = prepare_data()
    url = "http://127.0.0.1:8000/apirecord/"

    myobj = {
        'lecture_id': lecture_id,
        'report_data': json.dumps(report_data)
    }

    x = requests.post(url, json=myobj)
    print(x.text)

    return report_data

# if /shutdown is fetched the flask app will shutdown
@app.route('/shutdown')
def shutdown():
    print("Shut Down Initiating...")
    os.kill(os.getpid(), signal.SIGINT)
    return "Done"

### Socket Route
# Our flask app is connected to its webpage JS via websockets, this is how images are sent between the two places
# /identify is the socket route that is connected and images are sent to
@sock.route('/identify')
def identify(sock):
    img_path = 'image_before.png'
    num_eyes = 0

    while True:
        data = sock.receive() # data comes in as a data url
        
        response = urllib.request.urlopen(data)
        ## open the data URL 
        with open(img_path, 'wb') as f:
            f.write(response.file.read())
            # write it to a file

        # run face detection
        faces_array, front_faces, profile_faces, faces_perCapture = face_detect(img_path)
        return_url = image_to_data_url("image_after.png")
        emotion_array = check_emotions(faces_array)

        emotion_list.extend(emotion_array)
        
        # run the detection functions on the cropped small images
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

        # clean up and delete all images
        os.remove("image_after.png")
        os.remove("image_before.png")
        os.chdir("./flask-app/faces")
        files = os.listdir()
        for file in files:
            os.remove(file)
        os.chdir("../..")

if __name__ == "__main__":
     app.run(host="127.0.0.1", port=5000, debug=False)