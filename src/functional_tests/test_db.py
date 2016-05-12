from account.management.commands.createpublicanonuser import(
    create_public_user, create_anonymous_user)
from .base import FunctionalTest


class LoginTest(FunctionalTest):

    def test_create_delete_some_repos(self):
        good_repo_names = ['nospace', 'alph4numeric', 'middle_underscore']

        # Justin signs up and in
        self.sign_up_manually()

        for repo_name in good_repo_names:
            self.create_repo(repo_name)

        for repo_name in good_repo_names:
            self.delete_repo(repo_name)

    def test_cannot_create_bad_repos(self):
        bad_repo_names = ['one space', '_introUnderscore', 'semi;colon']

        # Justin sign up and in
        self.sign_up_manually()

        for name in bad_repo_names:
            # He clicks the add repo button
            self.browser.find_element_by_xpath(
                '(//a[@title="Create a New Repository"])[1]').click()

            # type the new repo id
            self.browser.find_element_by_id('new_repo_name').send_keys(name)

            # click create
            self.browser.find_element_by_id('new_repo_create').click()

            # the page says error
            page_source = self.browser.page_source
            self.assertTrue('Bad Request' in page_source)

            # he goes to the main page
            self.browser.get(self.server_url + '/browse/' + self.username)

            # the repo does not appear
            no_repo = self.browser.find_elements_by_link_text(name)
            self.assertEqual(no_repo, [])

    def test_create_some_tables(self):
        good_table_names = ['nospace', 'alph4numeric', 'middle_underscore']
        repo_name = 'repo_name'

        self.sign_up_manually()
        self.create_repo(repo_name)

        for table_name in good_table_names:
            self.create_table(repo_name, table_name)

    def test_create_some_views(self):
        good_view_names = ['nospace', 'alph4numeric', 'middle_underscore']
        repo_name = 'repo_name'
        table_name = 'table_name'

        self.sign_up_manually()
        self.create_repo(repo_name)
        self.create_table(repo_name, table_name)

        for view_name in good_view_names:
            self.create_view(
                repo_name, table_name, view_name)

    def test_public_repo(self):
        # Django migrations.RunPython doesn't happen before each test.
        # To work around this we call some methods (that should have been done
        # in migrations) here.
        # Django 1.8/1.9 https://code.djangoproject.com/ticket/23640
        create_public_user(None, None)
        create_anonymous_user(None, None)

        public_repo = 'public_repo'
        private_repo = 'private_repo'

        public_table = 'topsecretlol'
        private_table = 'corruptionnstuff'

        ed = 'delete_me_esnowden'
        laura = 'delete_me_lpoitras'

        # laura makes herself a datahub account
        self.sign_up_manually(username=laura, password=None)
        self.sign_out_manually()

        # ed makes himself a datahub account
        self.sign_up_manually(username=ed, password=None)

        # ed decides to make some repos
        self.create_repo(public_repo, ed)
        self.create_repo(private_repo, ed)

        # ed makes some tables, and shares their repo just with laura
        self.create_table(private_repo, private_table, ed)
        self.add_collaborator(private_repo, laura)

        # he makes some tables in a different repo, and makes the repo public
        self.create_table(public_repo, public_table, ed)
        self.make_repo_public(public_repo)

        # ed logs out
        self.sign_out_manually()

        # laura logs in and can see the repo. she clicks on it
        self.sign_in_manually(laura)
        self.browser.get(self.server_url + '/browse/' + ed)
        self.browser.find_element_by_link_text(private_repo).click()

        # she sees a shared table
        self.browser.find_element_by_link_text(private_table)

        # If she goes to the public url, she doesn't see the repo
        self.browser.get(self.server_url + '/browse/' + 'public')
        try:
            self.browser.find_element_by_link_text(private_repo)
            self.fail()
        except:
            pass

        # ... but can see the public repo
        self.browser.find_element_by_link_text(public_repo)

        # Laura signs out, and then goes back to the public url.
        # Even though She she isn't authenticated, she can still see the public
        # repo, and click on it.
        self.sign_out_manually()
        self.browser.get(self.server_url + '/browse/' + 'public')
        self.browser.find_element_by_link_text(public_repo).click()

    def test_add_remove_collaborator(self):
        # must be lowercase
        eazyE = 'delete_me_eazye'
        dre = 'delete_me_dre'
        snoop = 'delete_me_snoop'

        # can be uppercase
        repos = ['efil4zaggin', 'tsosn', 'sukka']
        tables = ['dopeman', 'thapolice']

        # print('eazyE joins datahub')
        self.sign_up_manually(username=eazyE, password=None)
        self.sign_out_manually()

        # print('snoop joins datahub')
        self.sign_up_manually(username=snoop, password=None)
        self.sign_out_manually()

        # print('dre joins datahub')
        self.sign_up_manually(username=dre, password=None)

        # print('dre creates repos and puts tables in them')
        for repo in repos:
            self.create_repo(repo, dre)

            for table in tables:
                self.create_table(repo, table, dre)

        # print('dre adds eazyE as a collabortor to one repo')
        self.add_collaborator(repos[0], eazyE)

        # print('dre logs out')
        self.sign_out_manually()

        # print('eazyE logs in')
        self.sign_in_manually(eazyE)

        # print('eazyE goes to the dre url')
        self.browser.get(self.server_url + '/browse/' + dre)

        # print('eazyE does not see repo[1], which is not shared')
        try:
            self.browser.find_element_by_link_text(repos[1])
            self.fail()
        except:
            pass

        # print('eazyE sees ginjuice, which is shared, and clicks on it')
        self.browser.find_element_by_link_text(repos[0]).click()

        # print('eazyE sees that the tables are shared')
        table_0 = self.browser.find_element_by_link_text(tables[0])
        table_1 = self.browser.find_element_by_link_text(tables[1])

        self.assertNotEqual(table_0, None)
        self.assertNotEqual(table_1, None)

        # print('eazyE clicks on a table')
        table_0.click()

        # print('the url matches')
        regex = (r'/browse/{user}/{repo}/table/{table}'
                 .format(user=dre, repo=repos[0], table=tables[0]))
        self.assertRegexpMatches(self.browser.current_url, regex)

        # print('eazyE is a sneaky mother'
        #       'he tries to get early access to dre\'s "beautiful" repo'
        #       'jerry put him up to')
        sneaky_url = ('{base}/browse/{user}/{repo}/tables'
                      .format(base=self.server_url, user=dre, repo=repos[1]))
        self.browser.get(sneaky_url)

        # print('the page says not found.')
        page_source = self.browser.page_source.lower()
        search_string = 'not found'
        self.assertTrue(search_string in page_source)

        # print('eazyE gives up. He goes to the homepage, logs out'
        #       'and takes a smoke break.')
        self.browser.get(self.server_url + '/browse/' + eazyE)
        self.sign_out_manually()

        # print('Dre gets word of what\'s happening. He signs back in')
        self.sign_in_manually(dre)

        # print('And Dre removes eazyE\'s access')
        self.remove_collaborator(repo=repos[0], collaborator=eazyE)

        # print('Dre then adds eazyE to the repo, sukka')
        self.add_collaborator(repos[2], eazyE)

        # print('Dre heads out. He\'s got some work to do')
        self.sign_out_manually()

        # print('eazyE logs in and goes to the dre url')
        self.sign_in_manually(eazyE)
        self.browser.get(self.server_url + '/browse/' + dre)

        # print('eazyE doesn\'t see repos[0], which dre removed his rights to')
        try:
            self.browser.find_element_by_link_text(repos[0])
            self.fail()
        except:
            pass

        # print('eaxyE does see \'sukka\' (repo[2])')
        self.browser.find_element_by_link_text(repos[2])

        # print('He tries to sneak into tSoSN (repos[0]), '
        #       'but can\'t get in either.')
        sneaky_url = ('{base}/browse/{user}/{repo}/tables'
                      .format(base=self.server_url, user=dre, repo=repos[0]))
        self.browser.get(sneaky_url)

        # print('the page says no table')
        page_source = self.browser.page_source.lower()
        # It's unclear why, but the test environment uses a different
        # template when raising 404 than the production env. Instead of
        # searching for 404, search for 'not found'.
        search_string = 'not found'
        self.assertTrue(search_string in page_source)

        # print('eazyE sends a diss to snoop')
        eazyE_repo = 'its_on_repo'
        self.create_repo(eazyE_repo, eazyE)
        self.create_table(
            repo_name=eazyE_repo, table_name='its_on_table', username=eazyE)
        self.add_collaborator(eazyE_repo, 'delete_me_snoop')

        # print('eazyE is all alone. No one loves him anymore.')
        # print('he is sad, but doesn\'t show it')
        # print('eazyE logs out')
        self.sign_out_manually()

        # print('snoop signs in')
        self.sign_in_manually(snoop)

        # print('snoop creates a repo, and puts a table in it')
        snoop_repo = 'hazy_ideas'
        snoop_table = 'rhymes'
        self.create_repo(snoop_repo, snoop)
        self.create_table(
            repo_name=snoop_repo, table_name=snoop_table, username=snoop)

        # print('snoop shares the repo with dre')
        self.add_collaborator(snoop_repo, dre)

        # print('snoop and dre are ready for the next episode.'
        #       'snoop deletes his acount')
        self.delete_account()

        # print('eazye signs in')
        self.sign_in_manually(username=eazyE)

        # print('eazye clicks on his dis repo collaborators. '
        #       'He sees that it isn\'t shared with snoop anymore.')
        xpath = ('(//table/tbody/tr[td/a/text()="{repo}"]/td/a[text()['
                 'contains(.,"collaborator(s)")]])[1]').format(repo=eazyE_repo)
        self.browser.find_element_by_xpath(xpath).click()
        page_source = self.browser.page_source
        self.assertFalse(snoop in page_source)

        # print('eazye is done. He deletes his account')
        self.delete_account()

        # print('dre logs in, and deletes his account too.')
        self.sign_in_manually(username=dre)
        self.delete_account()

        # eazyE and Dre aren't friends anymore.
