$(function() {
    /* Animating links on hover */

    $('.bouncing-links').hover(function(){ //Animate on hover
        $(this).addClass('animated shake')
    },
    function(){ //Remove animation when mouse moves out
        $(this).removeClass('animated shake')
    });
});
