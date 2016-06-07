from django.db.models import signals
from django.test import TestCase
from django.core.urlresolvers import resolve

from django.contrib.auth.models import User
from account.views import login, register, logout

import factory


class LoginPageTest(TestCase):

    @factory.django.mute_signals(signals.pre_save)
    def setUp(self):
        self.username = "delete_me_login_username"
        self.password = "delete_me_password"
        self.email = "test_email@csail.mit.edu"
        self.user = User.objects.create_user(
            self.username, self.email, self.password)

    def test_login_url_resolves_to_login_page_view(self):
        found = resolve('/account/login')
        self.assertEqual(found.func, login)

    def test_login_page_returns_correct_template(self):
        response = self.client.get('/account/login', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')


class RegisterPageTest(TestCase):

    def test_register_url_resolves_to_register_page_view(self):
        found = resolve('/account/register')
        self.assertEqual(found.func, register)

    def test_register_page_returns_correct_template(self):
        response = self.client.get('/account/register', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')


class LogoutPageTest(TestCase):

    @factory.django.mute_signals(signals.pre_save)
    def setUp(self):
        self.username = "delete_me_logout_username"
        self.password = "delete_me_password"
        self.email = "test_email@csail.mit.edu"
        self.user = User.objects.create_user(
            self.username, self.email, self.password)

    def test_logout_url_resolves_to_logout_page_view(self):
        found = resolve('/account/logout')
        self.assertEqual(found.func, logout)

    @factory.django.mute_signals(signals.pre_save)
    def test_logout_page_returns_correct_template(self):
        # log the user in
        self.client.login(username=self.username, password=self.password)

        # logout should return the home page
        response = self.client.get('/account/logout', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    @factory.django.mute_signals(signals.pre_save)
    def test_logout_page_actually_logs_users_out(self):
        # This isn't really the best test, but it seems dastardly difficult
        # to actually such a simple things properly.
        # I can only seem to verify whether a user is logged in or out
        # via the request object
        # The SO answers about is_authenticated aren't helpful, since
        # it returns true for all users who exist (but aren't logged in)

        # log the user in
        self.client.login(username=self.username, password=self.password)

        # make sure the user's actually logged in
        self.assertTrue(self.client.session.get('_auth_user_id'))

        # log the user out
        self.client.get("/account/logout", follow=True)

        # make sure the user is actually logged out
        self.assertEqual(self.client.session.get('_auth_user_id'), None)
