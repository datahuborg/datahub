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

class CardTests(TestCase):
    """test saving and loading cards"""

    def test_for_fields(self):
        initial_card = Card(id=10, repo_base="repo_base", repo_name="repo_name",
            card_name="card_name", query="query").save()
        loaded_card=Card.objects.get(id=10)

        self.assertEqual(loaded_card.id, 10)
        self.assertEqual(loaded_card.repo_base, "repo_base")
        self.assertEqual(loaded_card.repo_name, "repo_name")
        self.assertEqual(loaded_card.card_name, "card_name")
        self.assertEqual(loaded_card.query, "query")

class DashboardTest(TestCase):
    """test saving and loading dashboards

        This section left untestef for now, because
        I can't tell what Dashboards or Dashboard
        Cards are used for, or whether they're necessary
    """

class DashboardCardTest(TestCase):
    """test saving and loading dashboards

        This section left untestef for now, because
        I can't tell what Dashboards or Dashboard
        Cards are used for, or whether they're necessary
    """


class AnnotationTest(TestCase):
    """test saving and loading annotation"""

    def test_for_fields(self):
        initial_annotation = Annotation(id=10, url_path="url_path", 
            annotation_text="annotation_text").save()
        loaded_annotation = Annotation.objects.get(id=10)

        self.assertEqual(loaded_annotation.id, 10)
        self.assertEqual(loaded_annotation.url_path, "url_path")
        self.assertEqual(loaded_annotation.annotation_text, "annotation_text")


class AppTest(TestCase):
    """test saving and loading apps"""   

    def setup(self):
       pass

    def testForFields(self):
        # the user should really be stubbed/mocked, but I haven't figured out 
        # how yet.
        User(id=10, username="user", password="pass", email="email", 
            f_name="f_name", l_name="l_name", active=True).save()
        load_user = User.objects.get(id=10)

        initial_app = App(app_id="app_id", id=10, app_name="app_name", 
            app_token="app_token", user=load_user).save()
        load_app = App.objects.get(id=10)

        self.assertEqual(load_app.id, 10)
        self.assertEqual(load_app.app_id, "app_id")
        self.assertEqual(load_app.app_name, "app_name")
        self.assertEqual(load_app.app_token, "app_token")
        self.assertEqual(load_app.user, load_user)

class PermissionTest(TestCase):
    def setup(self):
        pass

    def testForFields(self):
        # the user should really be stubbed/mocked, but I haven't figured out 
        # how yet.
        User(id=10, username="user", password="pass", email="email", 
            f_name="f_name", l_name="l_name", active=True).save()
        load_user = User.objects.get(id=10)
        App(app_id="app_id", id=10, app_name="app_name", 
            app_token="app_token", user=load_user).save()
        load_app = App.objects.get(id=10)

        Permission(id=10, user=load_user, app=load_app,
            access=True).save()
        load_permission_true = Permission.objects.get(id=10)
        self.assertEqual(load_permission_true.user, load_user)
        self.assertEqual(load_permission_true.app, load_app)
        self.assertEqual(load_permission_true.access, True)


        Permission(id=11, user=load_user, app=load_app).save()
        load_permission_false = Permission.objects.get(id=11)
        self.assertEqual(load_permission_false.user, load_user)
        self.assertEqual(load_permission_false.app, load_app)
        self.assertEqual(load_permission_false.access, False)
