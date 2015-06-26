from django.test import TestCase
from inventory.models import *

class UserTests(TestCase):
    def test_fields(self):
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

class CardTests(TestCase):
    """test saving and loading cards"""

    def test_fields(self):
        initial_card = Card(id=10, repo_base="repo_base", repo_name="repo_name",
            card_name="card_name", query="query").save()
        loaded_card=Card.objects.get(id=10)

        self.assertEqual(loaded_card.id, 10)
        self.assertEqual(loaded_card.repo_base, "repo_base")
        self.assertEqual(loaded_card.repo_name, "repo_name")
        self.assertEqual(loaded_card.card_name, "card_name")
        self.assertEqual(loaded_card.query, "query")

class AnnotationTest(TestCase):
    """test saving and loading annotation"""

    def test_fields(self):
        initial_annotation = Annotation(id=10, url_path="url_path", 
            annotation_text="annotation_text").save()
        loaded_annotation = Annotation.objects.get(id=10)

        self.assertEqual(loaded_annotation.id, 10)
        self.assertEqual(loaded_annotation.url_path, "url_path")
        self.assertEqual(loaded_annotation.annotation_text, "annotation_text")


class AppTest(TestCase):
    """test saving and loading apps"""   

    def setUp(self):
        self.user, created = User.objects.get_or_create(id=10, username="user", password="pass", email="email", 
            f_name="f_name", l_name="l_name", active=True)


    def test_fields(self):
        app, created = App.objects.get_or_create(app_id="app_id", id=10, 
            app_name="app_name", app_token="app_token", user=self.user)

        self.assertEqual(app.id, 10)
        self.assertEqual(app.app_id, "app_id")
        self.assertEqual(app.app_name, "app_name")
        self.assertEqual(app.app_token, "app_token")
        self.assertEqual(app.user, self.user)

class PermissionTest(TestCase):
    """test permissions granted to apps"""

    def setUp(self):
        self.user, created = User.objects.get_or_create(id=10, username="user", password="pass", email="email", 
            f_name="f_name", l_name="l_name", active=True)

        self.app, created = App.objects.get_or_create(app_id="app_id", id=10, 
            app_name="app_name", app_token="app_token", user=self.user)

    def test_fields(self):
        permission, created = Permission.objects.get_or_create(id=10, user=self.user, app=self.app, access=True)

        self.assertEqual(permission.user, self.user)
        self.assertEqual(permission.app, self.app)
        self.assertEqual(permission.access, True)


    def test_defaults(self):
        permission, created = Permission.objects.get_or_create(id=11, 
            user=self.user, app=self.app)

        self.assertEqual(permission.access, False)
