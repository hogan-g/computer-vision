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
    side_column.innerHTML = "";
    list.innerHTML = "";
    
    data = JSON.parse(ev.data);
    console.log(data)

    photo.setAttribute("src", data["picture"]);

    small_pics = data["urls"]
    total_faces += data["faces"]
    total_profiles += data["profiles"]
    total_eyes += data["eyes"]

    for (let i = 0; i < small_pics.length; i++){
        img = document.createElement("img");
        img.src = small_pics[i];
        side_column.appendChild(img);
    }

    emotions = data["emotions"]
    for (let i = 0; i < emotions.length; i++){
        item = document.createElement("li");
        text = document.createTextNode(emotions[i]);
        item.appendChild(text);
        list.appendChild(item)
    }

    sessionStorage.setItem('num_eyes', data["eyes"]);
    sessionStorage.setItem('num_profiles', data["profiles"])
    sessionStorage.setItem('num_faces', data["faces"]);

    document.getElementById('curr_faces').innerHTML = "Faces: " + data["faces"]
    document.getElementById('curr_profiles').innerHTML = "Side Faces: " + data["profiles"]
    document.getElementById('curr_eyes').innerHTML = "Eyes: " + data["eyes"]

    // update data
    document.getElementById("total-faces").innerHTML = "Total Num of Faces Detected: " + total_faces;
    document.getElementById("total-profiles").innerHTML = "Total Num of Profiles Detected: " + total_profiles;
    document.getElementById("captures").innerHTML = "Num of Captures Taken: " + n_captures;
    document.getElementById("total-eyes").innerHTML = "Total Num of Eyes Detected: " + total_eyes;
    
    let average = Math.round(total_faces / n_captures);
    document.getElementById("average-faces").innerHTML = "Average Num of Faces: " + average;
});

function startup() {
    // grab elements of page to edit and add to
    video = document.getElementById("video");
    canvas = document.getElementById("canvas");
    photo = document.getElementById("photo");
    side_column = document.getElementById('side-column');
    list = document.getElementById('list');

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

    // buttons

    pic_button = document.getElementById('camera-button');
    start_button = document.getElementById('start-repeating');
    stop_button = document.getElementById('stop-repeating');

    pic_button.addEventListener(
        "click",
        (ev) => {
          takepicture();
          ev.preventDefault();
        },
        false
    );

    start_button.addEventListener(
        "click",
        (ev) => {
          repeater = setInterval(takepicture, 1000);
          chart_updater = setInterval(updateChart, 1000);
          ev.preventDefault();
        },
        false
    );

    stop_button.addEventListener(
        "click",
        (ev) => {
          clearInterval(repeater);
          clearInterval(chart_updater);
          ev.preventDefault();
        },
        false
    );

    clearphoto();

    google.charts.load("current", {
        packages: ["corechart", "line"]
    });
    
    google.charts.setOnLoadCallback(drawChart);

}

function drawChart() {
    // create data object with default value
    globalThis.chart_data = google.visualization.arrayToDataTable([
      ['Time', 'Eyes Detected', 'Faces Detected'],
      [0, 0, 0],
    ]);
    // create options object with titles, colors, etc.
    let options = {
      title: "Detections",
      hAxis: {
        textPosition: 'none',
      },
      vAxis: {
        title: "Number"
      }
    };
    // draw chart on load
    let chart = new google.visualization.LineChart(
      document.getElementById("chart_div")
    );
    chart.draw(chart_data, options); 
}

function updateChart(){
    let maxDatas = 50;
    let options = {
        title: "Detections",
        hAxis: {
          textPosition: 'none',
        },
        vAxis: {
          title: "Number"
        }
    };

    let num_eyes = parseInt(sessionStorage.getItem('num_eyes'))
    let num_faces = parseInt(sessionStorage.getItem('num_faces'))

    let chart = new google.visualization.LineChart(
        document.getElementById("chart_div")
    );

    if (chart_data.getNumberOfRows() > maxDatas) {
      chart_data.removeRows(0, chart_data.getNumberOfRows() - maxDatas);
    }
    chart_data.addRow([index, num_eyes, num_faces]);
    chart.draw(chart_data, options);
    index++;
}


function clearphoto() {
    const context = canvas.getContext("2d");
    context.fillStyle = 'cyan';
    context.fillRect(0, 0, canvas.width, canvas.height);

    const image_src = canvas.toDataURL("image/png");
    photo.setAttribute("src", image_src);
}

function takepicture() {
    n_captures += 1;

    const context = canvas.getContext("2d");
    if (width && height) {
        canvas.width = width;
        canvas.height = height;
        context.drawImage(video, 0, 0, width, height);

        const image_src = canvas.toDataURL("image/png");
        socket.send(image_src)
    } 
    else {
        clearphoto();
    }
}

window.addEventListener("load", startup, false);
