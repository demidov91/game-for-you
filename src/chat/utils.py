from django.core.paginator import Paginator
from django.contrib.syndication.views import Feed

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


class ChatFeed(Feed):
    def item_title(self, item):
        return item.author.userprofile.get_short_name()

    def item_description(self, item):
        return item.text

    def item_guid(self, item):
        return str(item.id)

def get_message_page(message):
    """
    message: *chat.Message* entity.
    returns: *int*, page number on which this **message** is expected to be. min value is 1.
    """
    return Message.objects.filter(chat=message.chat, create_time__lt=message.create_time).count() // MESSAGES_PER_PAGE + 1
