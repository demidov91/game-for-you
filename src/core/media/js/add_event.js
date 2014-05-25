$(function(){
    $('.change-view').click(function(){
        if ($('#add-event-wrapper').hasClass('competition')){
            $('#add-event-wrapper.competition').removeClass('competition').addClass('tournament');
        } else if ($('#add-event-wrapper').hasClass('tournament')){
            $('#add-event-wrapper.tournament').removeClass('tournament').addClass('competition');
        }
    });
});
