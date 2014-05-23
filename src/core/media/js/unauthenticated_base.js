$(function(){
    $('#email-authentication.force-show').modal();
    $('#email-authentication').on('submit', 'form', function(event){
        event.preventDefault();
        var jThis = $(this);
        var formData = jThis.serialize();
        var url = this.action;
        var method = this.method;
        $.ajax({
            url: url,
            method: method,
            data: formData,
            success: function(data){
                window.location.replace(data.location);
            },
            error: function(data){
                jThis.parent('div.toLeft').html(data.responseJSON.html);
            }
        });
        return false;
    });
    load_html_content($('#login-placeholder'), function(){
        $('#login-placeholder input[name="next"]').val(window.location.pathname + window.location.search);        
    });
    load_html_content($('#register-placeholder'));
});
