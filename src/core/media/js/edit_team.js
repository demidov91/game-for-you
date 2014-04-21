$(function(){
    var deleteTeamButton = $('#delete-team-button-wrapper>button');
    if (!deleteTeamButton.attr('disabled') == 'disabled'){
        load_html_content($('#delete-team-modal'));
    }

});