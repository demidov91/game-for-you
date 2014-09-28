/**
* Requires base.js script and ajaxPageUrlBase variable defined.
*/

function updatePageNumber(){
    var page = $('.messages').data('page'); 
    history.pushState({page: page}, '', '?page=' + page);
}

function getAjaxPageUrl(page){
    return ajaxPageUrlBase + '?page=' + page;     
}

$(function(){
    if ($('.chat-placeholder').length == 0){return;}
    load_html_content($('.chat-wrapper'), {success: updatePageNumber});
    updateListWithFormAction($('.chat-placeholder'), $('.chat-wrapper'), {success: updatePageNumber});
    $('.chat-placeholder').on('click', '.chat-page-links a', function(event){
        event.preventDefault();
        load_html_content($('.chat-wrapper').data('url', getAjaxPageUrl($(this).data('page'))), {
            success: updatePageNumber
        });
    });

    window.onpopstate = function(event){
        load_html_content($('.chat-wrapper').data('url', getAjaxPageUrl(event.state.page)));
    }

});
