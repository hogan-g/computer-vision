
const width = 320; // We will scale the photo width to this
let height = 0; // This will be computed based on the input stream

let streaming = false;

let video = null;
let canvas = null;
let photo = null;

const socket = new WebSocket('ws://127.0.0.1:5000/echo');

socket.addEventListener('message', ev => {
    photo.setAttribute("src", ev.data);
});

function startup() {
    video = document.getElementById("video");
    canvas = document.getElementById("canvas");
    photo = document.getElementById("photo");

    navigator.mediaDevices
    .getUserMedia({ video: true, audio: false })
    .then((stream) => {
        video.srcObject = stream;
        video.play();
    })
    .catch((err) => {
        console.error(`An error occurred: ${err}`);
    });

    video.addEventListener(
    "canplay",
    (ev) => {
        if (!streaming) {
        height = video.videoHeight / (video.videoWidth / width);

        video.setAttribute("width", width);
        video.setAttribute("height", height);
        canvas.setAttribute("width", width);
        canvas.setAttribute("height", height);
        streaming = true;
        }
    },
    false
    );

    clearphoto();
}


function clearphoto() {
    const context = canvas.getContext("2d");
    context.fillStyle = "#FFF";
    context.fillRect(0, 0, canvas.width, canvas.height);

    const data = canvas.toDataURL("image/png");
    photo.setAttribute("src", data);
}

function takepicture() {
    const context = canvas.getContext("2d");
    if (width && height) {
        canvas.width = width;
        canvas.height = height;
        context.drawImage(video, 0, 0, width, height);

        const data = canvas.toDataURL("image/png");
        socket.send(data)
    } 
    else {
        clearphoto();
    }
}

setInterval(function(){ 
    takepicture() 
}, 1000);

window.addEventListener("load", startup, false);
