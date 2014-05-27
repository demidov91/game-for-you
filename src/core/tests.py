from datetime import datetime

from django.test import TestCase
from django.utils import timezone

from core import utils
from core.factories import UserFactory
from core.models import ShareTree


class Utilstest(TestCase):
    def test_to_timestamp(self):
        expected_timestamp = 1390653930.0
        source_date = datetime(2014, 1, 25, 12, 45, 30, tzinfo=timezone.UTC())
        self.assertEqual(expected_timestamp, utils.to_timestamp(source_date))

    def test_user_mock(self):
        user_mock = utils.UserMock()
        self.assertFalse(user_mock.is_authenticated())
        user_mock._is_authenticated = True
        self.assertTrue(user_mock.is_authenticated())

    def test_string_types(self):
        self.assertTrue(isinstance(u'', utils.string_types))
        self.assertTrue(isinstance('', utils.string_types))


class UtilShareTreeTest(TestCase):
    def setUp(self):
        tree = []
        users = []
        for x in range(0, 6):
            users.append(UserFactory())
        tree.append(ShareTree.objects.create(shared_to=users[0]))
        tree.append(ShareTree.objects.create(shared_to=users[1], parent=tree[0]))
        tree.append(ShareTree.objects.create(shared_to=users[2], parent=tree[0]))
        tree.append(ShareTree.objects.create(shared_to=users[3], parent=tree[2]))
        tree.append(ShareTree.objects.create(shared_to=users[4]))
        tree.append(ShareTree.objects.create(shared_to=users[5], parent=tree[4]))
        self.test_trees = tree
        self.test_users = users

    def test_find_from_leaf_to_root(self):
        tested = utils.ShareTreeUtil()
        self.assertEqual(self.test_trees[0],
                         tested.find_from_leaf_to_root(self.test_trees[3], self.test_users[0]))
        self.assertEqual(self.test_trees[4],
                         tested.find_from_leaf_to_root(self.test_trees[5], self.test_users[4]))

    def test_find_from_leaf_to_root_cant_find(self):
        tested = utils.ShareTreeUtil()
        self.assertFalse(tested.find_from_leaf_to_root(self.test_trees[5], self.test_users[0]))

    def test_find_leaf_by_user(self):
        tested = utils.ShareTreeUtil()
        self.assertEqual(self.test_trees[3], tested.find_leaf_by_owner(self.test_trees[0], self.test_users[3]))


