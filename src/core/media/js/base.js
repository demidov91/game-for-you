function initialize_default_calendar(extraOptions){
        var calendarOptions = {
            events: getEventsUrl,            
            monthNames: monthNames,
            firstDay: 1,            
            dayNamesShort: dayNamesShort,
            dayClick: function(date){
                var day = date.getDate();
                var month = parseInt(date.getMonth()) + 1;
                var year = parseInt(date.getYear()) + 1900;
                $('.one-day-view').show();
                $('.observing-date').removeClass('observing-date');
                $(this).addClass('observing-date');
                $('#timestamp-to-create-event').val(date.getTime() / 1000 - 60 * date.getTimezoneOffset());
                $.ajax({
                    url: eventsForDay + 'day='+ day + '&month=' + month + '&year=' + year,
                    success: function(data){
                        $('.day-events').html(data);
                    }
                });
            }                 
        }
        $.extend(calendarOptions, extraOptions);
        
        var currentOptions = $.extend({}, calendarOptions);
        $.extend(currentOptions, {
            titleFormat: 'MMMM yyyy',
            header: {left: '', center: 'title', right: ''}
        });
        var afterOptions = $.extend({}, calendarOptions);
        $.extend(afterOptions, {
            titleFormat: 'MMMM yyyy',
            header: {left: '', center: 'title', right: ''}
        });

        $('.calendar-current').fullCalendar(currentOptions);
        $('.calendar-current .fc-header-left').text('‹').addClass('pointer').click(function(){
            $('#calendars>.fc').fullCalendar('prev');
        });
        $('.calendar-after').fullCalendar(afterOptions);
        $('.calendar-after').fullCalendar('next');
        $('.calendar-after .fc-header-right').text('›').addClass('pointer').click(function(){
            $('#calendars>.fc').fullCalendar('next');
        });
        $('.one-day-view .close').click(function(){
            $('.one-day-view').hide();
            $('.observing-date').removeClass('observing-date');
        });
}


function load_html_content(jObject, callback){
    $.ajax({
        url: jObject.data('url'),
        success: function(data){
            jObject.html(data);
        },
        complete: function(){
            if (callback) {callback();}
        }
    });
}

function getCSRF(){
    return $('input[name="csrfmiddlewaretoken"]').val();
}
