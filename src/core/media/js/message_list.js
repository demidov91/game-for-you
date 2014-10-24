/**
* Requires base.js script and ajaxPageUrlBase variable defined.
*/

firstVisit = true;
prevPage = 62000;

function updatePageNumber(){
    var page = $('.messages').data('page'); 
    if (firstVisit){
        history.replaceState({page: page}, '', '?page=' + page + location.hash);
        firstVisit = false;
    } else {
        history.pushState({page: page}, '', '?page=' + page);
    }
}

function getAjaxPageUrl(page){
    return ajaxPageUrlBase + '?page=' + page;     
}

function onPageChage(){
    updatePageNumber();
    var currentPage = parseInt($('.messages').data('page'));
    if (currentPage < prevPage){
        $("html").animate({scrollTop: $('.messages').position().top - 200 }, 500);
    }
    prevPage = currentPage;
}

function onSubmit(){
    updatePageNumber();
    CKEDITOR.instances['id_text'].updateElement();
    CKEDITOR.instances['id_text'].setData('');
    $('#id_text').val('');
}

function onInitialPageLoad(){
    updatePageNumber();
    if (location.hash.length > 0){
        $(location.hash)[0].scrollIntoView();
    }
}

$(function(){
    if ($('.chat-placeholder').length == 0){return;}
    load_html_content($('.chat-wrapper'), {success: onInitialPageLoad});
    loadListWithFormAction($('.chat-placeholder'), $('.chat-wrapper'), $('.chat-placeholder'), {success: onSubmit});
    $('.chat-placeholder').on('click', '.chat-page-links a', function(event){
        event.preventDefault();
        load_html_content($('.chat-wrapper').data('url', getAjaxPageUrl($(this).data('page'))), {
            success: onPageChage
        });
    });

    window.onpopstate = function(event){
        load_html_content($('.chat-wrapper').data('url', getAjaxPageUrl(event.state.page)));
    }

});
