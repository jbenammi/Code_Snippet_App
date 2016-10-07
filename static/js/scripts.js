$(document).ready(function(){
    console.log('jQuery on tap')

    $.ajaxPrefilter(function( options, originalOptions, jqXHR ) {
    options.async = true;
    });
    
    $.get('/notes/html', function(res){
        $('#right-box').html(res)
    }, 'html')//get end


    $(document).on('submit', "#code-form", function(){
        $.post('/get_update', $(this).serialize(), function(res){

            var button = $("#create-form").find('button');
                $(button).html('Update your Snippet')

            $('#input-textarea').html(res.cur_snippet['code']);
            $("input[name='description']").prop("value", res.cur_snippet['description']);
            $("input[name='snippet']").prop("value", res.cur_snippet['id']);
        }, 'json')//post end
        return false

    })//codeform submit end


});

jQuery(document).on("mouseenter mouseleave", ".snippet", function(){
    var updater = $(this).find(".update");
        $(updater).toggleClass("update-visible");
})//end change
