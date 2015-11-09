import hashlib

from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import resolve

from core.db.manager import DataHubManager
from django.contrib.auth.models import User
from browser.views import home
from browser.views import repo_create

class BrowserPagesNotRequiringAuth(TestCase):
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
# you may need to log into postgres and
# drop database username;
# drop role username;


class CreateAndDeleteRepo(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)

        # create the user
        self.username = "test_username"
        self.password = "test_password"
        self.email = "test_email@csail.mit.edu"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.hashed_password = hashlib.sha1(self.password).hexdigest()

        # create user's database
        DataHubManager.create_user(username=self.username, password=self.hashed_password)
        
        # log the user in
        self.client.login(username=self.username, password=self.password)

    def tearDown(self):
        # remove the postgres db. User will log out automatically.
        DataHubManager.remove_user_and_database(username=self.username)

    def test_create_repo_resolves_to_create_func(self):
        try:
            found = resolve('/create/' + self.username+ '/repo/')
        except:
            self.fail("exception at test_create_repo_resolves_to_create_func hit")

        self.assertEqual(found.func, repo_create)

    def test_create_repo_returns_correct_page(self):
        try:
            login_credentials = {'login_id': self.username, 
            'login_password': self.password}

            response = self.client.get('/create/' + self.username + '/repo', follow=True)
        except:
            self.fail("exception at test_create_repo_returns_correct_page hit")

        self.assertTemplateUsed(response, 'repo-create.html')

    def test_create_repo_creates_a_repo(self):
        try:
            # create the new repo
            post_object = {'repo': 'repo_name'}
            response = self.client.post('/create/' + self.username + '/repo', post_object)

            # get a list of repos that the user owns
            # import pdb; pdb.set_trace()
            manager = DataHubManager(user=self.username)
            res = manager.list_repos() 
            repos = [t[0] for t in res['tuples']]

            # make sure that it's in there
        except:
            self.fail("exception at test_create_repo_creates_a_repo")

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

