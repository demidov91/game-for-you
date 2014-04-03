/**
Requires variables: getEventsUrl.
**/


$(function(){
    $('.calendar-before').fullCalendar({
        events: getEventsUrl
    }).prev();
    $('.calendar-current').fullCalendar({
        events: getEventsUrl
    });
    $('.calendar-after').fullCalendar({
        events: getEventsUrl
    }).next();

    
});
