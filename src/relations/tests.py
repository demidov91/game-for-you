from django.test import TestCase
from django.contrib.auth import get_user_model

from relations.utils import create_team


class Utilstest(TestCase):
    def test_create_team(self):
        owner = get_user_model().objects.create()
        team_created = create_team(owner)
        self.assertEqual(team_created, owner.userprofile.primary_team)

