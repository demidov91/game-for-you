$(function(){
    $('.datetimepicker').datetimepicker({
        format: 'd.m.Y H:i',
        language: $('html').data('lang') 
    });
    
}); 


function loadListWithFormAction(jPlaceholder, jList, jFormsContainer){
    jFormsContainer.on('submit', 'form', function(event){
        event.preventDefault();
        jPlaceholder.addClass('loading'); 
        var jThis = $(this);
        jThis.ajaxSubmit({
            success: function(data){
                jList.html(data);
            },
            complete: function(){
                jPlaceholder.removeClass('loading');
            }
        });
        return false;
    });  
}

function updateListWithFormAction(jPlaceholder, jList){
    loadListWithFormAction(jPlaceholder, jList, jList);    
}

