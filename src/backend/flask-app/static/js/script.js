const width = 320; // We will scale the photo width to this
let height = 0; // This will be computed based on the input stream

// setup some variables for data tracking
let n_captures = 0;
let total_faces = 0;
let total_profiles = 0;
let total_eyes = 0;

let streaming = false;

let video = null;
let canvas = null;
let photo = null;

let index = 0;  

const socket = new WebSocket('ws://127.0.0.1:5000/identify');

socket.addEventListener('message', ev => { // function for when data is received in socket, also updates page variables and data
    
    data = JSON.parse(ev.data);
    console.log(data)

    photo.setAttribute("src", data["picture"]);
});

const sleep = (milliseconds) => {
    return new Promise(resolve => setTimeout(resolve, milliseconds))
}

// function to shutdown the flask app
async function shutdown(){
    fetch("/results")
	.then(response => response.json())
	.then(data => console.log(data),
        await sleep(1000),
        fetch("/shutdown")
        .then(
            await sleep(1000),
            window.close()
        )
    );
}

function startup() {
    // grab elements of page to edit and add to
    video = document.getElementById("video");
    canvas = document.getElementById("canvas");
    photo = document.getElementById("photo");
    side_column = document.getElementById('side-column');
    list = document.getElementById('list');

    // grab the users camera device
    navigator.mediaDevices
    .getUserMedia({ video: true, audio: false })
    .then((stream) => {
        video.srcObject = stream;
        video.play();
    })
    .catch((err) => {
        console.error(`An error occurred: ${err}`);
    });

    // once the camera can stream, display the vide stream
    video.addEventListener(
    "canplay",
    (ev) => {
        if (!streaming) {
        height = video.videoHeight / (video.videoWidth / width);

        video.setAttribute("width", width*1.5);
        video.setAttribute("height", height*1.5);
        canvas.setAttribute("width", width);
        canvas.setAttribute("height", height);
        streaming = true;
        }
    },
    false
    );

    // buttons

    pic_button = document.getElementById('camera-button');
    start_button = document.getElementById('start-repeating');
    stop_button = document.getElementById('stop-repeating');

    // take a test picture when this button is pressed
    pic_button.addEventListener(
        "click",
        (ev) => {
          takepicture();
          ev.preventDefault();
        },
        false
    );

    // when the start auto capture button is pressed, take a picture every one second
    start_button.addEventListener(
        "click",
        (ev) => {
          repeater = setInterval(takepicture, 1000);
          document.getElementById("capture-status").style = "color:green; text-decoration: none; margin-bottom: 0%;"
          ev.preventDefault();
        },
        false
    );

    // when the stop button is pressed, remove the interval triggering takepicture()
    stop_button.addEventListener(
        "click",
        (ev) => {
          clearInterval(repeater);
          document.getElementById("capture-status").style = "color:red; text-decoration: line-through; margin-bottom: 0%;"
          ev.preventDefault();
        },
        false
    );

    clearphoto();

}

// clears the preview image off the screen
function clearphoto() {
    const context = canvas.getContext("2d");
    context.fillStyle = 'transparent';
    context.fillRect(0, 0, canvas.width, canvas.height);

    const image_src = canvas.toDataURL("image/png");
    photo.setAttribute("src", image_src);
}

function takepicture() {
    // tracks how many pictures have been taken
    n_captures += 1;

    const context = canvas.getContext("2d");
    // if the video is there
    if (width && height) {
        canvas.width = width;
        canvas.height = height;
        context.drawImage(video, 0, 0, width, height);
        // takes an image from the video and draws it to a canvas

        const image_src = canvas.toDataURL("image/png");
        // converts the canvas to an image dataUrl 
        socket.send(image_src)
        //sends the dataURL via websocket
    } 
    else {
        clearphoto();
    }
}

// when the window loads, call the startup() function
window.addEventListener("load", startup, false);
