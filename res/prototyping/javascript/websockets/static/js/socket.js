const socket = new WebSocket('ws://127.0.0.1:5000/echo');
socket.onopen = function (event) {
    socket.send("Hello World")
};
socket.addEventListener('message', ev => {
    console.log(ev.data);
});