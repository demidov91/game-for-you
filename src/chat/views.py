from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator

from chat.models import TagMessage
from chat.forms import TagMessageForm
from chat.utils import get_message_count_for_tag_page
from tournament.models import Tag


def tag_chat(request, tag_id):
    """
    ajax view.
    request: POST for new message. GET accepts *page* parameter.
    returns: chat part of some page.
    """
    tag = get_object_or_404(Tag.objects, id=tag_id)
    if request.method == 'POST':
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        form = TagMessageForm(request.POST, request.user, tag)
        if form.is_valid():
            form.save()
            return redirect('tag_chat', tag_id=tag.id)
    else:
        form = TagMessageForm()
    paginator = Paginator(TagMessage.objects.filter(tag=tag), get_message_count_for_tag_page(request, tag_id))
    page_number = int(request.GET.get('page') or paginator.num_pages)
    print(page_number)
    return render(request, 'parts/tag_message_list.html', {
        'form': form,
        'tag': tag,
        'page': paginator.page(page_number),
        'is_authenticated': request.user.is_authenticated,
    })



