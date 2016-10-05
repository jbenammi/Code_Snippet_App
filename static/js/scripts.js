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

    



});

//
// <form method="POST">
//  <div id="edit" name="edit" style="height: 300px"></div>
// </form>
