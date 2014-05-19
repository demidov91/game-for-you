from datetime import datetime

from django.test import TestCase
from django.utils import timezone

from core.utils import to_timestamp


class Utilstest(TestCase):
    def test_to_timestamp(self):
        expected_timestamp = 1390653930.0
        source_date = datetime(2014, 1, 25, 12, 45, 30, tzinfo=timezone.UTC())
        self.assertEqual(expected_timestamp, to_timestamp(source_date))
