from .base import FunctionalTest
import pages
from urllib import urlencode
from urlparse import urlparse, parse_qs
import requests


class APITest(FunctionalTest):

    def test_authorization_code_flow(self):
        user_info = {
            'username': 'delete_me_test',
            'email': 'delete_me_test@mit.edu',
            'password': 'delete_me_test',
        }
        client_info = {
            'name': 'Test App',
            'client_type': 'confidential',
            'authorization_type': 'code',
            # redirect_uri needs to be to the server because PhantomJS doesn't
            # like POST redirects to external hosts. Luckily these OAuth tests
            # just need to grab the authorization code from the URL. It doesn't
            # matter if the redirect is really followed.
            'redirect_uri': self.server_url + '/gibberishURLForTestClient/',
        }

        # Go directly to the sign up page
        self.browser.get(self.server_url + '/account/register')
        registration_page = pages.RegistrationPage(self.browser)
        # Create a new user
        registration_page.fill_in_form(**user_info)
        browse_page = registration_page.submit_form()
        # Verify the account was created by seeing if we're on the browse page.
        self.assertRegexpMatches(
            self.browser.current_url, r'/browse/',
            msg="Failed to register user {0}".format(user_info['username']))

        # Register a new OAuth client app as that user
        apps_page = browse_page.go_to_create_app()
        create_oauth_app_page = apps_page.go_to_register_app()
        create_oauth_app_page.fill_in_form(**client_info)
        app_page = create_oauth_app_page.submit_form()
        # Save this new client's details for later
        client_info.update(app_page.client_details())
        # Log the user out
        self.browser.get(self.server_url + '/')
        browse_page = pages.BrowsePage(self.browser)
        browse_page.go_to_sign_out()
        self.assertRegexpMatches(
            self.browser.current_url, r'/www/',
            msg="Failed to log out user. "
                "Should have been sent to the home page.")

        # Now pretend to be that client app and ask the user to grant it
        # authorization.
        params = {
            'response_type': 'code',
            'client_id': client_info['client_id'],
            'redirect_uri': client_info['redirect_uri'],
            'scope': 'read write',
        }
        # Send user to authorization page
        authz_url = "/oauth2/authorize/?" + urlencode(params)
        self.browser.get(self.server_url + authz_url)
        # Should first be redirected to login
        self.assertRegexpMatches(
            self.browser.current_url, r'/account/login\?next',
            msg="Should have been asked to log in first.")
        # Log in
        login_page = pages.LoginPage(self.browser)
        login_page.fill_in_form(**user_info)
        login_page.submit_form()
        # Should end up at the authorization page after a successful login
        self.assertRegexpMatches(
            self.browser.current_url, r'/oauth2/authorize',
            msg="Should have been redirected to the authorization page.")
        authz_page = pages.AuthorizationPage(self.browser)
        # Deny access first
        authz_page.cancel()
        # Should be sent to redirect_uri with an error=access_denied.
        self.assertEqual(
            self.browser.current_url,
            client_info['redirect_uri'] + "?error=access_denied",
            msg="Should have been redirected to "
                "the client's redirect URI on \"Cancel\".")

        # Send user to authorization page again
        self.browser.get(self.server_url + authz_url)
        # Allow access this time
        authz_page.authorize()
        # Should be sent to redirect_uri with an auth code.
        self.assertRegexpMatches(
            self.browser.current_url, client_info['redirect_uri'],
            msg="Should have been redirected to "
                "the client's redirect URI on \"Authorize\".")

        # Pull the authorization code out of the redirect URL
        redirect_url = self.browser.current_url
        query = parse_qs(urlparse(redirect_url).query)
        self.assertIn('code', query,
                      msg="Authorization redirect should include a code.")
        auth_code = query['code']

        # Exchange the authorization code for an access token
        params = {
            'code': auth_code,
            'client_id': client_info['client_id'],
            'client_secret': client_info['client_secret'],
            'redirect_uri': client_info['redirect_uri'],
            'grant_type': 'authorization_code',
        }
        token_url = self.server_url + "/oauth2/token/"
        request = requests.post(token_url, data=params)
        self.assertEqual(200, request.status_code)
        token_response = request.json()
        self.assertIn('access_token', token_response)
        access_token = token_response['access_token']

        # Test an API endpoint without using the access token
        request = requests.get(self.server_url + '/api/v1/user/')
        self.assertEqual(401, request.status_code)

        # Test an API endpoint using a gibberish access token
        headers = {'Authorization': 'Bearer not1a2real3token'}
        request = requests.get(self.server_url + '/api/v1/user/',
                               headers=headers)
        self.assertEqual(401, request.status_code)

        # Test an API endpoint using the real access token
        headers = {'Authorization': 'Bearer ' + access_token}
        request = requests.get(self.server_url + '/api/v1/user/',
                               headers=headers)
        self.assertEqual(200, request.status_code)
        response = request.json()
        self.assertIn('username', response)
        self.assertEqual(user_info['username'], response['username'])

        # Revoke that token
        # User is still logged in, no need to log in again
        self.browser.get(self.server_url + '/')
        browse_page = pages.BrowsePage(self.browser)
        settings_page = browse_page.go_to_settings()
        token_page = settings_page.go_to_token_management()
        # Make sure there's only the one token we asked for
        revocation_links = token_page.token_revocation_links()
        self.assertEqual(1, len(revocation_links))
        revocation_links[0].click()
        # Confirm deletion
        confirm_page = pages.TokenRevocationPage(self.browser)
        token_page = confirm_page.confirm_revocation()
        # Make sure it's gone now
        revocation_links = token_page.token_revocation_links()
        self.assertEqual(0, len(revocation_links))

        # Test an API endpoint using the revoked access token
        request = requests.get(self.server_url + '/api/v1/user/',
                               headers=headers)
        self.assertEqual(401, request.status_code)

        # Go to user's home page
        self.browser.get(self.server_url + '/')
        browse_page = pages.BrowsePage(self.browser)
        # Go to settings
        settings_page = browse_page.go_to_settings()
        # Delete that user
        settings_page.delete_account()
