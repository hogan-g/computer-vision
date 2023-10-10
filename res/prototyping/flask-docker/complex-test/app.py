from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

camera = cv2.VideoCapture(-1)
cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #change to grayscale

            faces = faceCascade.detectMultiScale( #experiment with different numbers in here
                gray,
                scaleFactor=1.1, # adjusts for further away and back
                # detection algorithm uses a window to search, minsize is the size of the window
                # minNeighbours gives how many things need to be detected to declare a face
                minNeighbors=5,
                minSize=(30, 30),
            )

            for (x, y, w, h) in faces: # draw rectangles around faces
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)


            err, buffer = cv2.imencode('.jpg', frame) # encode the frame as a jpg
            
            if not err:
                break
            else:
                frame = buffer.tobytes() #translate to bytes
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)