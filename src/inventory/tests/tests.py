from django.test import TestCase
from inventory.models import *

class UserTests(TestCase):
    def test_for_fields(self):
        """ saving and loading users"""

        initial_user = User(id=10, username="user", password="pass", email="email", 
            f_name="f_name", l_name="l_name", active=True).save()
        loaded_user = User.objects.get(id=10)

        self.assertEqual(loaded_user.id, 10)
        self.assertEqual(loaded_user.username, "user")
        self.assertEqual(loaded_user.password, "pass")
        self.assertEqual(loaded_user.email, "email")
        self.assertEqual(loaded_user.f_name, "f_name")
        self.assertEqual(loaded_user.l_name, "l_name")
        self.assertEqual(loaded_user.active, True)
        self.assertEqual(unicode(loaded_user), "user")

# class CardTests(TestCase):
#     """test saving and loading cards"""

#     initial_card = Card(id=1, repo_base="repo_base", repo_name="repo_name",
#         card_name="card_name", query="query").save()
#     loaded_card=Card.objects.get(id=1)

#     self.assertEqual(loaded_card.card_name, "card_name")





