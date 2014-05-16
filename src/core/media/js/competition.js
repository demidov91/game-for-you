$(function(){
    load_html_content($('#competition-participants'));
    updateListWithFormAction($('#competition-participants-placeholder'), $('#competition-participants'));

    $('#competition-participants-placeholder').on('click', '.team-to-add-source', function(){
        var jThis = $(this);
        $('.team-to-add-destination').val(jThis.data('team-id'));
        jThis.parents('form').submit();
    });
});
