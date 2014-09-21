/**
* Requires base.js script and ajaxPageUrlBase variable defined.
*/

function updatePageNumber(){
    var page = $('.tag-messages').data('page'); 
    history.pushState({page: page}, '', '?page=' + page);
}

function getAjaxPageUrl(page){
    return ajaxPageUrlBase + '?page=' + page;     
}

$(function(){
    initialize_default_calendar();
    if ($('#tag-chat-placeholder').length == 0){return;}
    load_html_content($('#tag-chat-wrapper'));
    updateListWithFormAction($('#tag-chat-placeholder'), $('#tag-chat-wrapper'), { success: updatePageNumber});
    $('#tag-chat-placeholder').on('click', '#tag-chat-page-links a', function(event){
        event.preventDefault();
        load_html_content($('#tag-chat-wrapper').data('url', getAjaxPageUrl($(this).data('page'))), {
            success: updatePageNumber
        });
    });

    window.onpopstate = function(event){
        load_html_content($('#tag-chat-wrapper').data('url', getAjaxPageUrl(event.state.page)));
    }
});
