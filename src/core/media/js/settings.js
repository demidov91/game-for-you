$(function(){
    $('#select-place').change(function(){
        $('#places-forms .one-form').removeClass('show');
        $('#places-forms #place-' + this.value).addClass('show');
    }).change();
});
