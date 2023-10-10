from flask import Flask, render_template, Response
from flask_sock import Sock
import base64
import cv2
import urllib

app = Flask(__name__)
sock = Sock(app)

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

def face_detect(path):  
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #change to grayscale

    faces = faceCascade.detectMultiScale( #experiment with different numbers in here
        gray,
        scaleFactor=1.1, # adjusts for further away and back
        minNeighbors=5,
        minSize=(30, 30),
    )

    for (x, y, w, h) in faces: # draw rectangles around faces
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    path = 'image_after.png'
    cv2.imwrite(path, img)

    img_url = image_to_data_url(path)
    return img_url
    
def image_to_data_url(filename):
    ext = filename.split('.')[-1]
    prefix = f'data:image/{ext};base64,'
    with open(filename, 'rb') as f:
        img = f.read()
    return prefix + base64.b64encode(img).decode('utf-8')

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@sock.route('/echo')
def echo(sock):
    img_path = 'image_before.png'
    while True:
        data = sock.receive() # data comes in as a data uri

        response = urllib.request.urlopen(data)
        with open(img_path, 'wb') as f:
            f.write(response.file.read())

        return_url = face_detect(img_path)
        sock.send(return_url)
        


# 1. grab image from js
# 2. send it via websocket base 64 encoded
# 3. run facial rec on it
# 4. send it back, display it

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)