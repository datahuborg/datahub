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
# if these fail because a role/database already exists
# you will need to log into postgres and
# drop database username;
# drop role username;

class CreateAndDeleteRepo(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)

        # Need to mock out the authentication system here
        # So that we aren't actually testing the auth/db systems, too
        # ARC

        # create the user
        self.username = "username"
        self.password = "password"
        self.hashed_password = hashlib.sha1(self.password).hexdigest()
        DataHubManager.create_user(username=self.username, password=self.hashed_password)
        
        user = User(username=self.username, email="noreply@mit.edu", 
            password=self.hashed_password)
        user.save()
       
        # log the user in
        login_credentials = {'login_id': self.username, 
        'login_password': self.password}
        self.client.post('/account/login', login_credentials) 

    def tearDown(self):
        DataHubManager.remove_user_and_database(username=self.username)

    def test_create_repo_resolves_to_create_func(self):
        found = resolve('/create/' + self.username+ '/repo/')
        self.assertEqual(found.func, repo_create)

    def test_create_repo_returns_correct_page(self):
        login_credentials = {'login_id': self.username, 
        'login_password': self.password}

        response = self.client.get('/create/' + self.username + '/repo', follow=True)
        self.assertTemplateUsed(response, 'repo-create.html')


    def test_create_repo_creates_a_repo(self):
        # create the new repo
        post_object = {'repo': 'repo_name'}
        response = self.client.post('/create/' + self.username + '/repo', post_object)

        # get a list of repos that the user owns
        manager = DataHubManager(user=self.username)
        res = manager.list_repos() 
        repos = [t[0] for t in res['tuples']]

        # make sure that it's in there
        self.assertTrue('repo_name' in repos)

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