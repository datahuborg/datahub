from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


class BasePage(object):
    """
    Subclass to encapsulate page-specific behavior

    Takes the current webdriver.
    To use find_element(s), subclasses must override the locators dict.
    """

    locators = {}

    def __init__(self, driver):
        super(BasePage, self).__init__()
        self.driver = driver

    def find_element(self, locator):
        return self.driver.find_element(*self.locators[locator])

    def find_elements(self, locator):
        return self.driver.find_elements(*self.locators[locator])


class RegistrationPage(BasePage):
    """User registration / sign up page"""

    locators = {
        'username': (By.ID, 'id_username'),
        'email':    (By.ID, 'id_email'),
        'password': (By.ID, 'id_password'),
        'sign_up':  (By.ID, 'id_sign_up_action'),
    }

    def fill_in_form(self, username="", email="", password="", **kwargs):
        username_field = self.find_element('username')
        username_field.send_keys(username)
        email_field = self.find_element('email')
        email_field.send_keys(email)
        password_field = self.find_element('password')
        password_field.send_keys(password)

    def submit_form(self):
        self.find_element('sign_up').click()
        return BrowsePage(self.driver)


class LoginPage(BasePage):
    """User login / sign in page"""

    locators = {
        'username': (By.ID, 'id_username'),
        'password': (By.ID, 'id_password'),
        'sign_in':  (By.ID, 'id_sign_in_action'),
    }

    def fill_in_form(self, username="", password="", **kwargs):
        username_field = self.find_element('username')
        username_field.send_keys(username)
        password_field = self.find_element('password')
        password_field.send_keys(password)

    def submit_form(self):
        self.find_element('sign_in').click()
        return BrowsePage(self.driver)

    def already_logged_in(self):
        return 'Already logged in' in self.driver.page_source


class BrowsePage(BasePage):
    """General browsing page users are sent to after logging in"""

    locators = {
        'user_menu_link': (By.ID, 'id_user_menu'),
        'launch_terminal_link': (By.ID, 'id_launch_terminal'),
        'create_app_link': (By.ID, 'id_create_app'),
        'settings_link': (By.ID, 'id_settings'),
        'sign_out_link': (By.ID, 'id_sign_out'),
    }

    def _show_menu_if_not_displayed(self, element):
        menu = self.find_element('user_menu_link')
        if not element.is_displayed():
            menu.click()

    def go_to_launch_terminal(self):
        element = self.find_element('launch_terminal_link')
        self._show_menu_if_not_displayed(element)
        element.click()
        # return ConsolePage(self.driver)

    def go_to_create_app(self):
        element = self.find_element('create_app_link')
        self._show_menu_if_not_displayed(element)
        element.click()
        return AppsPage(self.driver)

    def go_to_settings(self):
        element = self.find_element('settings_link')
        self._show_menu_if_not_displayed(element)
        element.click()
        return SettingsPage(self.driver)

    def go_to_sign_out(self):
        element = self.find_element('sign_out_link')
        self._show_menu_if_not_displayed(element)
        element.click()
        # return HomePage(self.driver)


class SettingsPage(BasePage):
    """User account settings page"""

    locators = {
        'delete_account_button': (By.ID, 'id_delete_acct_button'),
        'confirm_delete_button': (By.ID, 'id_delete_confirm_button'),
        'manage_tokens_link': (By.LINK_TEXT, 'Manage active tokens'),
    }

    def delete_account(self):
        self.find_element('delete_account_button').click()
        self.find_element('confirm_delete_button').click()

    def go_to_token_management(self):
        self.find_element('manage_tokens_link').click()
        return TokenManagementPage(self.driver)


class TokenManagementPage(BasePage):
    """Page for managing active OAuth tokens"""

    locators = {
        'revoke_token_link': (By.LINK_TEXT, 'Revoke'),
    }

    def token_revocation_links(self):
        return self.find_elements('revoke_token_link')


class TokenRevocationPage(BasePage):
    """Confirmation page for revoking OAuth tokens"""

    locators = {
        'confirm_button': (By.XPATH, '//input[@value="Revoke"]'),
    }

    def confirm_revocation(self):
        self.find_element('confirm_button').click()
        return TokenManagementPage(self.driver)


class AppsPage(BasePage):
    """Client app management page"""

    locators = {
        'temporary_oauth_apps_link': (By.PARTIAL_LINK_TEXT, 'OAuth'),
        'register_app_link': (
            By.XPATH,
            '//a[@title="Register a New DataHub App"]'),
    }

    def go_to_register_app(self):
        self.find_element('register_app_link').click()
        return RegisterOAuthAppPage(self.driver)


class RegisterOAuthAppPage(BasePage):
    """OAuth client app registration page"""

    locators = {
        'name': (By.ID, 'id_name'),
        'client_type': (By.ID, 'id_client_type'),
        'authorization_grant_type': (By.ID, 'id_authorization_grant_type'),
        'redirect_uris': (By.ID, 'id_redirect_uris'),
        'save_button': (By.XPATH, '//*[text()="Save"]'),
    }

    def fill_in_form(self, name, client_type,
                     authorization_type, redirect_uri, **kwargs):
        name_field = self.find_element('name')
        name_field.send_keys(name)

        select = Select(self.find_element('client_type'))
        select.select_by_visible_text('Confidential')

        select = Select(
            self.find_element('authorization_grant_type'))
        select.select_by_visible_text('Authorization code')

        uris = self.find_element('redirect_uris')
        uris.send_keys(redirect_uri)

    def submit_form(self):
        self.find_element('save_button').click()
        return OAuthAppPage(self.driver)


class OAuthAppPage(BasePage):
    """OAuth client app detail page"""

    locators = {
        'client_id': (
            By.XPATH,
            '//div/p[label/text() = "Client ID"]/span'),
        'client_secret': (
            By.XPATH,
            '//div/p[label/text() = "Client Secret"]/span'),
    }

    def client_details(self):
        return {
            'client_id':
                self.find_element('client_id').text,
            'client_secret':
                self.find_element('client_secret').text,
        }


class AuthorizationPage(BasePage):
    """OAuth user authorization page"""

    locators = {
        'authorize_button': (By.XPATH, '//*[@value="Authorize"]'),
        'cancel_button': (By.XPATH, '//*[@value="Cancel"]'),
    }

    def authorize(self):
        self.find_element('authorize_button').click()

    def cancel(self):
        self.find_element('cancel_button').click()
