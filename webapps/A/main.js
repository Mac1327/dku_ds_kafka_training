document.querySelector('.video').style.visibility = "hidden";

$('.boton-url').on('click',function(){
    var theURL = getWebAppBackendUrl('haar_video')
    console.log(theURL)
    document.querySelector('.video').src = theURL  
    document.querySelector('.video').style.visibility = "visible";
});