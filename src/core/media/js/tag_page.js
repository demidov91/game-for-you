$(function(){
    initialize_default_calendar();
    if ($('#tag-chat-placeholder').length == 0){return;}
    load_html_content($('#tag-chat-wrapper'));
    updateListWithFormAction($('#tag-chat-placeholder'), $('#tag-chat-wrapper'));
});
