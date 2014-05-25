$(function(){
    $('input#id_tags_request').tagit({
        autocomplete: {
            source: getTagsAutocompeteUrl,
            minLength: 1,
        },
        singleFieldDelimiter: ", "       
    });
});
