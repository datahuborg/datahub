import hashlib

from django.test import TestCase
from django.test import Client
from django.http import HttpRequest
from django.core.urlresolvers import resolve

from inventory.models import User
from account.auth import login, register, clear_session, logout, forgot, verify, reset, jdbc_password 


class LoginPageTest(TestCase):

    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.user, created = User.objects.get_or_create(id=10, username="user", 
            password="pass", email="noreply.csail.mit.edu", f_name="f_name", l_name="l_name", 
            active=True)

    def test_login_url_resolves_to_login_page_view(self):
        found = resolve('/account/login')
        self.assertEqual(found.func, login)

    def test_login_page_returns_correct_template(self):
        response = self.client.get('/account/login', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_page_allows_user_to_login(self):
        login_credentials = {'login_id': self.user.username, 
        'login_password': self.user.password}
        response = self.client.post('/account/login', login_credentials) 
        
        self.assertEqual(response.status_code, 200)
        self.fail('test not completed. Users the test creates cannot \
            authenticate because their password hashes will not match.')


class RegisterPageTest(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        
    def test_register_url_resolves_to_register_page_view(self):
        found = resolve('/account/register')
        self.assertEqual(found.func, register)

    def test_register_page_returns_correct_template(self):
        response = self.client.get('/account/register', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_page_allows_new_user_registration(self):
        self.fail('test not yet implemented')

    def test_registered_user_actually_exists(self):
        self.fail('test not yet implemented')


class LogoutPageTest(TestCase):
    def setUp(self):
         self.client = Client(enforce_csrf_checks=False)
         # create a new user

    def test_logout_url_resolves_to_logout_page_view(self):
        found = resolve('/account/logout')
        self.assertEqual(found.func, logout)

    def test_logout_page_returns_correct_template(self):
        response = self.client.get('/account/logout')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confirmation.html')

    def test_logout_page_actually_logs_users_out(self):
        self.fail('test not yet implemented')


class ForgotPasswordPageTest(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        # create a new user

    def test_forgot_password_page_resolves_to_forgot_page_view(self):
        found = resolve('/account/forgot')
        self.assertEqual(found.func, forgot)

    def test_forgot_password_page_returns_correct_template(self):
        response = self.client.get('/account/forgot', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forgot.html')

    def test_forgot_post_with_valid_email(self):
        # test is incomplete. requires a user in the database
        # response = self.client.post('/account/forgot', {'email', 'goodemailhere@mydomain.yes'})
        # self.assertEqual(response.status_code, 200)
        self.fail('test not yet implemented')

    def test_forgot_post_bad_email(self):
        self.fail('test not yet implemented')


class JdbcPasswordTest(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        # create a new user

    def test_jdbc_password_unauthenticated(self):
        # test that this redirects unauthentiated users to the login page
        response = self.client.get('/account/jdbc_password', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_jdbc_password_unauthenticated(self):
        # test is incomplete. it should check to make sure the password
        # hashing is correct.
        response = self.client.get('/account/jdbc_password', follow=True)
        self.assertEqual(response.status_code, 200)
        self.fail('test not yet implemented')

class ResetPasswordTest(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        # create a new user

    def test_reset_password(self):
        # response = self.client.post('/account/reset', 
        #     {'user_email': '', 'new_password': 'smith'})
        # self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'login.html')
        self.fail('test not yet implemented')

