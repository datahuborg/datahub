import factory

from inventory import models

from django.test import TestCase
from django.db.models import signals
from django.db.utils import IntegrityError
from django.contrib.auth.models import User


class LegacyUserTests(TestCase):
    """Tests saving and loading legacy users."""

    def test_fields(self):
        models.DataHubLegacyUser.objects.create(
            id=10, email="foo@bar.fizz", username="delete_me_foobar",
            f_name="f_name", l_name="l_name", password="_h4rd;Pa_ss w-0Rd_",
            active=True)
        loaded_user = models.DataHubLegacyUser.objects.get(id=10)

        self.assertEqual(loaded_user.id, 10)
        self.assertEqual(loaded_user.email, "foo@bar.fizz")
        self.assertEqual(loaded_user.username, "delete_me_foobar")
        self.assertEqual(loaded_user.f_name, "f_name")
        self.assertEqual(loaded_user.l_name, "l_name")
        self.assertEqual(loaded_user.password, "_h4rd;Pa_ss w-0Rd_")
        self.assertEqual(loaded_user.active, True)
        self.assertEqual(unicode(loaded_user), "delete_me_foobar")


class CardTests(TestCase):
    """Test saving and loading cards."""

    def test_fields(self):
        models.Card.objects.create(
            id=10, repo_base="repo_base", repo_name="repo_name",
            card_name="card_name", query="query")

        loaded_card = models.Card.objects.get(id=10)

        self.assertEqual(loaded_card.id, 10)
        self.assertEqual(loaded_card.repo_base, "repo_base")
        self.assertEqual(loaded_card.repo_name, "repo_name")
        self.assertEqual(loaded_card.card_name, "card_name")
        self.assertEqual(loaded_card.query, "query")


class AnnotationTest(TestCase):
    """Test saving and loading annotations."""

    def test_fields(self):
        models.Annotation.objects.create(
            id=10, url_path="url_path", annotation_text="annotation_text")
        loaded_annotation = models.Annotation.objects.get(id=10)

        self.assertEqual(loaded_annotation.id, 10)
        self.assertEqual(loaded_annotation.url_path, "url_path")
        self.assertEqual(loaded_annotation.annotation_text, "annotation_text")


class AppTest(TestCase):
    """Test saving and loading apps."""

    @factory.django.mute_signals(signals.pre_save)
    def setUp(self):
        self.legacy_user = models.DataHubLegacyUser.objects.create(
            id=10, email="foo@bar.fizz", username="delete_me_foobar",
            f_name="f_name", l_name="l_name", password="_h4rd;Pa_ss w-0Rd_",
            active=True)

        self.user = User.objects.create_user(
            "delete_me_username", "email@email.email", "password")

    def test_fields(self):
        app = models.App.objects.create(
            app_id="app_id", id=10, app_name="app_name",
            app_token="app_token", user=self.user,
            legacy_user=self.legacy_user)

        self.assertEqual(app.id, 10)
        self.assertEqual(app.app_id, "app_id")
        self.assertEqual(app.app_name, "app_name")
        self.assertEqual(app.app_token, "app_token")
        self.assertEqual(app.legacy_user, self.legacy_user)
        self.assertEqual(app.user, self.user)


class CollaboratorTest(TestCase):
    """Test saving and loading collaborators."""

    @factory.django.mute_signals(signals.pre_save)
    def setUp(self):
        self.legacy_user = models.DataHubLegacyUser.objects.create(
            id=10, email="foo@bar.fizz", username="delete_me_foobar",
            f_name="f_name", l_name="l_name", password="_h4rd;Pa_ss w-0Rd_",
            active=True)

        self.user = User.objects.create_user(
            "delete_me_username", "email@email.email", "password")

        self.app = models.App.objects.create(
            app_id="app_id", id=10, app_name="app_name",
            app_token="app_token", user=self.user,
            legacy_user=self.legacy_user)

    def test_fields(self):
        collaborator = models.Collaborator.objects.create(
            id=10, user=self.user,
            repo_name='repo_name', repo_base='repo_base',
            permission='ALL')

        self.assertEqual(collaborator.user, self.user)
        self.assertEqual(collaborator.repo_name, 'repo_name')
        self.assertEqual(collaborator.repo_base, 'repo_base')
        self.assertEqual(collaborator.permission, 'ALL')

    def test_cannot_have_app_and_user(self):
        with self.assertRaises(IntegrityError):
            models.Collaborator.objects.create(
                id=10, user=self.user, app=self.app,
                repo_name='repo_name', repo_base='repo_base',
                permission='ALL')
