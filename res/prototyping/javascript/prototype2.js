navigator.mediaDevices.getUserMedia({video:true})
.then(function(stream) {
    var video = document.querySelector('video');
    video.srcObject = stream
    video.onloadedmetadata = function(e){
      video.play();
    };
})
.catch(function(err) {
  alert("Error", err)
});