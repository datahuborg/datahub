from django.test import TestCase

from django.test import Client

class SiteAccountPages(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        

    def test_login(self):
        # self.response = self.client.get(reverse('/'))
        # self.assertEqual(self.response.status_code, 200)
        # SimpleTestCase.assertContains(response, text, count=None, status_code=200, msg_prefix='', html=False)
        response = self.client.get('/account/login', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_register(self):
        response = self.client.get('/account/register', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_logout(self):
        # test that the page exists, not that it actually works
        response = self.client.get('/account/logout')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confirmation.html')

    def test_forgot_get(self):
        response = self.client.get('/account/forgot', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forgot.html')

    def test_forgot_post_bad_email(self):
        # tests that reset page can be posted to with wrong email addresses
        # response = self.client.post('/account/forgot', {'email', 'noemailhere@noreply.noo'})
        # self.assertEqual(response.status_code, 200)
        # returns a 403 due

        # self.assertTemplateUsed(response, 'forgot.html')
        pass

    def test_forgot_post_good_email(self):
        # test is incomplete. requires a user in the database
        # response = self.client.post('/account/forgot', {'email', 'goodemailhere@mydomain.yes'})
        # self.assertEqual(response.status_code, 200)
        pass


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

    def test_reset_password(self):
        # response = self.client.post('/account/reset', 
        #     {'user_email': '', 'new_password': 'smith'})
        # self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'login.html')
        pass


    def test_verify(self):
        pass






