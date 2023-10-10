# Contents

This directory is full of subdirectories with scripts and random bits and bobs that I used to learn and understand how to use the different technologies I needed to develop the software for our project, here is an overview of what is in each directory

- **docker** : contains a very simple dockerfile which I learned and experimented with
- **fix-emotion-detection** : this was used much later in development after we figured our our emotion detection was not working, we experimented with deepface as a different method in here
- **flask** : where I learned how to make a flask app, and eventually integrated our opencv script with the flask app
- **flask-docker** : this is where the more complex testing of combining flask and docker was done, /simple-test contains a very simple flask app that I was able to put into a docker container, then /complex-test introduces a more complex flask app using opencv, /old-version contains the flask app without facial rec that I got working with docker before combining with scripts in /flask and introducing the facial rec components
- **javascript** : this directory was used to work out how to use javascript to grab and take pictures with the webcam, instead of hardwiring it, in here is also where I first used websockets to connect the JS frontend to the Python backend, sending the images in between them for use in the facial recognition in the backend, and then displaying the results on the frontend browser
- **prog-opencv** : the oldest directory, it holds the initial scripts I made following a tutorial, and the git repo that the tutorial provided, I did a lot of tweaking and changing in here at the beginning to get opencv working initially
- **slicing_emotion** : this dir is where I initially experimented with how to crop smaller images out of the big image and then run eye and emotion detection on them
- **yolo** : contains files and resources from when I followed a tutorial using Yolo alongside opencv to do object detection, was not continued
