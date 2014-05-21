from datetime import datetime

from django.test import TestCase
from django.utils import timezone

from core import utils


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
