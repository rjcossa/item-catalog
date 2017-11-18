$(function() {
    $('.bouncing-links').hover(function(){ //Open on hover
        $(this).addClass('animated shake')
    },
    function(){ //Close when not hovered
        $(this).removeClass('animated shake')
    });
});
