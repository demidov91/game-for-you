function initialize_default_calendar(extraOptions){
        var calendarOptions = {
            events: getEventsUrl,            
            monthNames: monthNames,
            firstDay: 1,            
            dayNamesShort: dayNamesShort                      
        }
        $.extend(calendarOptions, extraOptions);
        
        var beforeOptions = $.extend({}, calendarOptions);
        $.extend(beforeOptions, {
            titleFormat: 'MMMM',
            header: {left: '', center: '', right: 'title'}
        });
        var currentOptions = $.extend({}, calendarOptions);
        $.extend(currentOptions, {
            titleFormat: 'MMMM yyyy',
            header: {left: '', center: 'title', right: ''}
        });
        var afterOptions = $.extend({}, calendarOptions);
        $.extend(afterOptions, {
            titleFormat: 'MMMM',
            header: {left: 'title', center: '', right: ''}
        });

        $('.calendar-before').fullCalendar(beforeOptions);
        $('.calendar-before').fullCalendar('prev');
        $('.calendar-before .fc-header-left').text('‹').addClass('pointer').click(function(){
            $('#calendars>.fc').fullCalendar('prev');
        });

        $('.calendar-current').fullCalendar(currentOptions);
        $('.calendar-after').fullCalendar(afterOptions);
        $('.calendar-after').fullCalendar('next');
        $('.calendar-after .fc-header-right').text('›').addClass('pointer').click(function(){
            $('#calendars>.fc').fullCalendar('next');
        });
}


function load_html_content(jObject){
    $.ajax({
        url: jObject.data('url'),
        success: function(data){
            jObject.html(data);
        }
    });
}
