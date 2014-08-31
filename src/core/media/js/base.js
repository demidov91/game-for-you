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

/**
* jPlaceholder: static jQuery element, which contains updateable list.
* jList: static jQuery element, which contains dynamic list elements.
* jFormsContainer: static jQuery element. All dynamic forms will be processed with ajax.
* ajaxParams: optional object with optional attributes 'success' and 'complete' for ajax events processing.
*  1st parameter will be form element, 2nd parameter will be ajax response data.  
*/
function loadListWithFormAction(jPlaceholder, jList, jFormsContainer, ajaxParams){
    jFormsContainer.on('submit', 'form', function(event){
        event.preventDefault();
        jPlaceholder.addClass('loading'); 
        var jThis = $(this);
        jThis.ajaxSubmit({
            success: function(data){
                jList.html(data);
                if (ajaxParams && ajaxParams.success){
                    ajaxParams.success(jThis, data);
                }
            },
            complete: function(){
                jPlaceholder.removeClass('loading');
                if (ajaxParams && ajaxParams.complete){
                    ajaxParams.complete(jThis);
                }
            }
        });
        return false;
    });  
}

function updateListWithFormAction(jPlaceholder, jList, ajaxParams){
    loadListWithFormAction(jPlaceholder, jList, jList, ajaxParams);    
}
