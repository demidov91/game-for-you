$(function(){
    $('#username-input').keyup(function(){
        var jThis = $(this);
        if (jThis.val().length > 1){
            $('#found-users-placeholder').addClass('loading');
            $.ajax({
                url: findPeopleByNameUrl,
                method: 'GET',
                data: {
                    contains: jThis.val()
                },
                success: function(data){
                    $('#found-users-list').html(data);
                },
                complete: function(){
                    $('#found-users-placeholder').removeClass('loading');
                }
            });
        } 
    });
    $('#found-users-placeholder').on('click', '.player', function(){
        var jThis = $(this);
        $('#contacts-placeholder').addClass('loading');    
        $.ajax({
            url: addContactUrl,
            method: 'POST',
            data: {
                userprofile_id: jThis.data('id'),
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val() 
            },
            success: function(data){
                $('#contacts-list').html(data);
            },
            complete: function(){
                $('#contacts-placeholder').removeClass('loading');
            }
        });
    });

    updateListWithFormAction($('#contacts-placeholder'), $('#contacts-list'));
});
