/**
* Returns unique css-selector for contact elevent with userprofile id specified.
*/
function getContactSelectorById(id){
    return '.contact-to-add-into-team.about-' + id; 
}

$(function(){
    var deleteTeamButton = $('#delete-team-button-wrapper>button');
    if (!deleteTeamButton.attr('disabled') == 'disabled'){
        load_html_content($('#delete-team-modal'));
    }
    updateListWithFormAction($('#team-members-placeholder'), $('#team-members'), {
        success: function(jThis){
            if (!jThis.hasClass('remove-from-team')){
                return;            
            }
            var id = jThis.parent('.member').data('id');
            $(getContactSelectorById(id)).removeClass('hidden');    
        }
    });
    
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
                jThis.addClass('hidden');
            },
            complete: function(){
                $('#team-members-placeholder').removeClass('loading');   
            }
        });        
    });

    $('#team-members .member').each(function(){
        $(getContactSelectorById($(this).data('id'))).addClass('hidden');    
    });

});
