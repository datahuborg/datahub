import hashlib

from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import resolve

from core.db.manager import DataHubManager
from inventory.models import User
from browser.views import home
from browser.views import repo_create

class BrowserPagesNotRequiringAuthentication(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)

    def test_home_url_resolves_to_home_func(self):
        found = resolve('/')
        self.assertEqual(found.func, home)

    def test_home_url_returns_index_template(self):
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


# tests below this comment require authentication

class CreateAndDeleteRepo(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)

        # create the user
        self.username = "myoneusername21"
        self.password = "password"
        self.hashed_password = hashlib.sha1("password").hexdigest()
        # self.user, created = User.objects.get_or_create(id=10, username="user", 
        #     password=self.hashed_password, email="noreply.csail.mit.edu", f_name="f_name", 
        #     l_name="l_name", active=True)
        DataHubManager.create_user(username=self.username, password=self.hashed_password)

        # log the user in
        login_credentials = {'login_id': self.username, 
        'login_password': self.password}
        self.client.post('/account/login', login_credentials) 

    def test_create_repo_resolves_to_create_func(self):
        found = resolve('/create/' + self.username+ '/repo')
        self.assertEqual(found.func, repo_create)

    # def test_create_repo_returns_correct_page(self):
    #     post_object = {'repo': 'sadflkw'}

    #     response = self.client.post('/create/myoneusername/repo', post_object)
    #     # self.assertEqual(1, 1)
    #     import pdb
    #     pdb.set_trace()
    #     self.assertTemplateUsed(response, 'repo-create.html')
        

    def createCard(self):
        pass

    def createAnotation(self):
        pass

    def deleteRepo(self):
        pass

    def deleteCard(self):
        pass

    def deleteAnnotation(self):
        pass