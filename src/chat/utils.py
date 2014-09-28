from django.core.paginator import Paginator

from chat.models import Message


MESSAGES_PER_PAGE = 20


def get_chat_page(chat, page_param):
    """
    chat: *chat.models.Chat* instance.
    page_param: page number parameter got from request. *str*. May be None.
    return: *django.core.paginator.Page* to show.
    """
    paginator = Paginator(Message.objects.filter(chat=chat), MESSAGES_PER_PAGE)
    return paginator.page(int(page_param or paginator.num_pages))


