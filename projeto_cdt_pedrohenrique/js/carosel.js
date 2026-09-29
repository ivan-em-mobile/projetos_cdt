let slideIndex = 1;

document.addEventListener("DOMContentLoaded", function () {

    showSlides(slideIndex);

    setInterval(() => {
        plusSlides(1);
    }, 5000);

});


function plusSlides(n) {
    showSlides(slideIndex += n);
}


function currentSlide(n) {
    showSlides(slideIndex = n);
}


function showSlides(n) {

    let slides = document.getElementsByClassName("slide");
    let dots = document.getElementsByClassName("dot");

    if (slides.length === 0) {
        return;
    }

    if (n > slides.length) {
        slideIndex = 1;
    }

    if (n < 1) {
        slideIndex = slides.length;
    }


    for (let i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }


    for (let i = 0; i < dots.length; i++) {
        dots[i].classList.remove("active");
    }


    slides[slideIndex - 1].style.display = "block";


    if (dots[slideIndex - 1]) {
        dots[slideIndex - 1].classList.add("active");
    }

}