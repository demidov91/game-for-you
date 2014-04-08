function initialize_default_calendar(){
        $('.calendar-before').fullCalendar({
            events: getEventsUrl,
            titleFormat: 'MMMM',
            monthNames: monthNames,
            firstDay: 1,
            header: {left: '', center: '', right: 'title'},
            dayNamesShort: dayNamesShort
        });
        $('.calendar-before').fullCalendar('prev');
        $('.calendar-before .fc-header-left').text('‹').addClass('pointer').click(function(){
            $('#calendars>.fc').fullCalendar('prev');
        });

        $('.calendar-current').fullCalendar({
            events: getEventsUrl,
            titleFormat: 'MMMM yyyy',
            monthNames: monthNames,
            firstDay: 1,
            header: {left: '', center: 'title', right: ''},
            dayNamesShort: dayNamesShort
        });
        $('.calendar-after').fullCalendar({
            events: getEventsUrl,
            titleFormat: 'MMMM',
            monthNames: monthNames,
            firstDay: 1,
            header: {left: 'title', center: '', right: ''},
            dayNamesShort: dayNamesShort
        });
        $('.calendar-after').fullCalendar('next');
        $('.calendar-after .fc-header-right').text('›').addClass('pointer').click(function(){
            $('#calendars>.fc').fullCalendar('next');
        });
}

