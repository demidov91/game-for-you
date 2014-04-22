$(function(){
    initialize_default_calendar({
        dayClick: function(date){
            $('.one-day-view').show();
            $.ajax({
                url: eventsForDay +
 'day='+date.getDate() + '&month=' + (parseInt(date.getMonth()) + 1) + '&year=' + (parseInt(date.getYear()) + 1900),
                success: function(data){
                    $('.day-events').html(data);
                }
            });
        }   
    });

    $('.one-day-view .close').click(function(){
        $('.one-day-view').hide();
    });
});
