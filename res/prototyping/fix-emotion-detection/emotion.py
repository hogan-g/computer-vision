import numpy as np
import cv2
from keras.models import load_model

img_array = ["test1.jpg","test2.jpg","test3.jpg","test4.jpg","test5.jpg","test6.jpg","test7.jpg","test8.jpg"]

for img in img_array:
    face_image = cv2.imread(img)
    face_image = cv2.resize(face_image, (48,48))
    face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
    face_image = np.reshape(face_image, [1, face_image.shape[0], face_image.shape[1], 1])

    emotion_dict= {'Angry': 0, 'Sad': 5, 'Neutral': 4, 'Disgust': 1, 'Surprise': 6, 'Fear': 2, 'Happy': 3}
    model = load_model("model_v6_23.hdf5")

    predicted_class = np.argmax(model.predict(face_image))
    label_map = dict((v,k) for k,v in emotion_dict.items()) 
    predicted_label = label_map[predicted_class]

    print(predicted_label)