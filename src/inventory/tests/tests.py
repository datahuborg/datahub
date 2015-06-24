from django.test import TestCase
from inventory.models import *

class UserTests(TestCase):
    def test_for_fields(self):
        """ saving and loading users"""

        initial_user = User(username="user", password="pass", email="email", 
            f_name="fname", l_name="lname", active=True).save()
        loaded_user = User.objects.get(username="user")

        self.assertEqual(loaded_user.username, "user")
        self.assertEqual(loaded_user.password, "pass")
        self.assertEqual(loaded_user.email, "email")
        self.assertEqual(loaded_user.f_name, "fname")
        self.assertEqual(loaded_user.l_name, "lname")
        self.assertEqual(loaded_user.active, True)
        self.assertEqual(unicode(loaded_user), "user")

class CardTests(TestCase):
    """test cards"""


