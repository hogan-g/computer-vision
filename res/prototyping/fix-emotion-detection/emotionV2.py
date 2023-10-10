from deepface import DeepFace

img_array = ["conall.jpg"]

for path in img_array:
    face_analysis = DeepFace.analyze(img_path = path, enforce_detection=False, actions = ['emotion', 'race', 'gender', 'age'])

    print(face_analysis)
