$(document).ready(function(){
    console.log('jQuery on tap')

    $.ajaxPrefilter(function( options, originalOptions, jqXHR ) {
    options.async = true;
    });

    $('.snippet').on("click", function(){
        console.log("hit");
        var updater = $(this).find(".update");
            $(updater).toggleClass("update-visible");
    });

    $.get('/notes/html', function(res){
        console.log(res)
        $('#right-box').html(res)
    }, 'html')//get end

});
