$(function(){
    $('#edit-owners').click(function(){
        $('#tag-accessors-management').removeClass('sharer-edit').addClass('owner-edit');
    });
    $('#stop-edit-owners').click(function(){
        $('#tag-accessors-management').removeClass('owner-edit');
    });
});
