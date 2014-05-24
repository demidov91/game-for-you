$(function(){
    load_html_content($('#managers .list-placeholder .list'));
    loadListWithFormAction($('#managers .list-placeholder'), $('#managers .list'), $('#contacts .list-placeholder'));

    $('#managers .list-placeholder').on('submit', 'form.make-owner', function(event){
        event.preventDefault();
        var jThis = $(this);
        $('#managers .list-placeholder').addClass('loading');
        jThis.ajaxSubmit({
            success: function(){
                jThis.parents('.item').removeClass('sharer').addClass('owner');
            },
            complete: function(){
                $('#managers .list-placeholder').removeClass('loading');
            }
        });
        return false;
    });
    $('#managers .list-placeholder').on('submit', 'form.make-sharer', function(event){
        event.preventDefault();
        var jThis = $(this);
        var redirect = false;
        if (jThis.parents('.me-owner').length == 1){
            if (confirm(confirmRemovingYourselfAsOwnerWords)){
                redirect = true;
            } else {
                return false;
            }
        }
        $('#managers .list-placeholder').addClass('loading');
        jThis.ajaxSubmit({
            success: function(){
                jThis.parents('.item').removeClass('owner').addClass('sharer');
                if (redirect){
                    window.location.href = redirectToAfterRemovingYourselfAsOwner;
                }
            },
            complete: function(){
                $('#managers .list-placeholder').removeClass('loading');
            }
        });
        return false;
    });
    $('#managers .list-placeholder').on('submit', 'form.remove', function(event){
        event.preventDefault();
        var jThis = $(this);
        

        $('#managers .list-placeholder').addClass('loading');
        jThis.ajaxSubmit({
            success: function(){
                jThis.parents('.item').hide();
            },
            complete: function(){
                $('#managers .list-placeholder').removeClass('loading');
            }
        });
        return false;
    });


    
});
