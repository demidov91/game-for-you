from django.test import TestCase

from core.utils import Mock, UserMock
from tournament import utils
from tournament.models import Tag

class SubscribedToMock:
    inner = None
    def __init__(self):
        self.inner = [Tag(name='example', id=1), Tag(name='example-2', id=2)]
    def all(self):
        return self.inner
    def add(self, x):
        self.inner.append(x)
    def remove(self, x):
        self.inner.remove(x)


class UtilTest(TestCase):
    def _get_request_mock(self):
        request_mock = Mock()
        request_mock.session = {}
        request_mock.user = UserMock()
        return request_mock

    def _get_tags_final_check(self, tested):
        tags = tested.get_tags()
        self.assertEqual(2, len(tags))
        for tag in tags:
            self.assertIsInstance(tag, Tag)

    def _add_tag_final_check(self, tested):
        tags = tested.get_tags()
        self.assertEqual(3, len(tags))
        for tag in tags:
            self.assertIsInstance(tag, Tag)

    def _remove_tag_final_check(self, tested):
        tags = tested.get_tags()
        self.assertEqual(1, len(tags))

    def _prepare_auth_tags_env(self):
        request = self._get_request_mock()
        request.user._is_authenticated = True
        request.user.subscribed_to = SubscribedToMock()
        return utils.AuthenticatedTagsProvider(request)

    def _prepare_nauth_tags_env(self):
        tag_ids = []
        for i in range(0, 2):
            tag_ids.append(Tag.objects.create(name='ttugtn-example-{0}'.format(i)).id)
        request = self._get_request_mock()
        request.session[utils.NoneAuthenticatedTagsProvider.SESSION_KEY] = tag_ids
        return utils.NoneAuthenticatedTagsProvider(request)

    def test_get_tags_provider(self):
        request = self._get_request_mock()
        self.assertIsInstance(utils.get_tags_provider(request), utils.NoneAuthenticatedTagsProvider)
        request.user._is_authenticated = True
        self.assertIsInstance(utils.get_tags_provider(request), utils.AuthenticatedTagsProvider)

    def test_get_tags_auth(self):
        tested = self._prepare_auth_tags_env()
        self._get_tags_final_check(tested)


    def test_get_tags_nauth(self):
        tested = self._prepare_nauth_tags_env()
        self._get_tags_final_check(tested)

    def test_add_tag_auth(self):
        tested = self._prepare_auth_tags_env()
        Tag.objects.create(name='example-3')
        tested.add_tag_by_name('example-3')
        self._add_tag_final_check(tested)

    def test_add_tag_nauth(self):
        tag_ids = []
        for i in range(0, 2):
            tag_ids.append(Tag.objects.create(name='ttuatn-example-{0}'.format(i)).id)
        request = self._get_request_mock()
        request.session[utils.NoneAuthenticatedTagsProvider.SESSION_KEY] = tag_ids
        tested = utils.NoneAuthenticatedTagsProvider(request)
        Tag.objects.create(name='example-4')
        tested.add_tag_by_name('example-4')
        self._add_tag_final_check(tested)

    def test_remove_tag_auth(self):
        tested = self._prepare_auth_tags_env()
        tested.user.subscribed_to.inner = [1, 2]
        tested.remove_tag_by_id(2)
        self._remove_tag_final_check(tested)

    def test_remove_tag_nauth(self):
        tested = self._prepare_nauth_tags_env()
        ids = tested.get_tags()
        tested.remove_tag_by_id(ids[0].id)
        self._remove_tag_final_check(tested)







