$(function(){
    initialize_default_calendar();
    $('#add-tag-name').autocomplete({
        source: getTagsAutocompeteUrl,
        minLength: 1,
        select: function(event, ui){
            $('#add-tag-name').val(ui.item.value);
            $('#add-tag-name').parents('form').submit();
        }
    });
    $('#not-popular-tags-header').click(function(){
        $('#not-popular-tags').slideToggle();
        $(this).toggleClass('dropup');
    });
});
