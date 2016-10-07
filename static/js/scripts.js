$(document).ready(function() {
    console.log('jQuery on tap')

    $.ajaxPrefilter(function(options, originalOptions, jqXHR) {
        options.async = true;
    });

    $.get('/notes/html', function(res) {
            $('#right-box').html(res)
        }, 'html') //get snippets end

    $.get('/notes/form', function(res) {
            $('#input-form').html(res);
        }, 'html') //get form end

    $(document).on('submit', "#code-form", function() {
            $.get('/notes/update_form', function(res) {
                    $('#input-form').html(res);
                }, 'html') //get update form end

            $.post('/get_update', $(this).serialize(), function(res) {
                    $('#input-textarea').html(res.cur_snippet['code']);
                    $("input[name='description']").prop("value", res.cur_snippet['description']);
                    $("input[name='snippet_id']").prop("value", res.cur_snippet['id']);
                    console.log(res.cur_snippet['id'])
                }, 'json') //end post
            return false
        }) //codeform submit end

    $(document).on('submit', "#update-form", function() {
            console.log('hit update')
            $.post('/update', $(this).serialize(), function(res) {
                console.log('hit post')
            })

            $.get('/notes/form', function(res) {
                    $('#input-form').html(res);
                }, 'html') //get form end
            console.log('hit form')

            $.get('/notes/html', function(res) {
                    $('#right-box').html(res)
                }, 'html') //get snippets end
            return false

        }) //end update


});

jQuery(document).on("mouseenter mouseleave", ".snippet", function() {
        var updater = $(this).find(".update");
        $(updater).toggleClass("update-visible");
    }) //end change
