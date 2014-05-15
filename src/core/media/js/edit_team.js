$(function(){
    var deleteTeamButton = $('#delete-team-button-wrapper>button');
    if (!deleteTeamButton.attr('disabled') == 'disabled'){
        load_html_content($('#delete-team-modal'));
    }
    updateListWithFormAction($('#team-members-placeholder'), $('#team-members'));
    
    $('.contact-to-add-into-team').click(function(){
        var jThis = $(this);
        $('#team-members-placeholder').addClass('loading');
        $.ajax({
            method: 'POST',
            url: jThis.data('add-into-team-url'),
            data: {
                csrfmiddlewaretoken: getCSRF()
            },
            success: function(data){
                $('#team-members').html(data);    
            },
            complete: function(){
                $('#team-members-placeholder').removeClass('loading');   
            }
        });
        
    });
    

});
