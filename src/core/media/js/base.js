function onCalendarResize(){
    var height = $('.calendar-current').height();
    $('.change-month').css('line-height', height + 'px');  
    $('.change-month').css('font-size', height / 3 + 'px');  
}

function initialize_default_calendar(extraOptions){
        var calendarOptions = {
            events: getEventsUrl,            
            monthNames: monthNames,
            firstDay: 1,            
            dayNamesShort: dayNamesShort,
            windowResize: onCalendarResize,
                loading: function(isLoading, view){view.element.parents('#calendars>div').toggleClass('loading', isLoading); 
            },
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
        
        $('.calendar-current').fullCalendar(currentOptions);
        onCalendarResize();
        $('#calendars>.prev').click(function(){
            $('#calendars>.fc').fullCalendar('prev');
        });
        $('#calendars>.next').click(function(){
            $('#calendars>.fc').fullCalendar('next');
        });
        $('.one-day-view .close').click(function(){
            $('.one-day-view').hide();
            $('.observing-date').removeClass('observing-date');
        });
}


function load_html_content(jObject, ajaxParams){
    jObject.parent().addClass('loading');
    $.ajax({
        url: jObject.data('url'),
        success: function(data){
            jObject.html(data);
            if (ajaxParams && ajaxParams.success){
                ajaxParams.success(data);
            }
        },
        complete: function(data){
            if (ajaxParams && ajaxParams.complete){
                ajaxParams.complete(data);
            }
            jObject.parent().removeClass('loading');            
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

//Do nothing if history api is not defined.
if (history){
    history = {
        pushState: function(){
            console.log('History API is not defined. Update your browser.');
        }
    }
}
