from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from inventory.models import App
from core.db.manager import DataHubManager
from django.core.validators import RegexValidator

from django.conf import settings


def validate_unique_username(value):
    """
    Validates that a proposed username is not already in use.

    Checks User and App models, databases, database roles, and user data
    folders.
    """
    username = value.lower()

    try:
        existing_user = User.objects.get(username=username)
    except User.DoesNotExist:
        existing_user = None

    try:
        existing_app = App.objects.get(app_id=username)
    except App.DoesNotExist:
        existing_app = None

    db_exists = DataHubManager.database_exists(username)
    user_exists = DataHubManager.user_exists(username)
    user_data_folder_exists = DataHubManager.user_data_folder_exists(username)

    if (existing_user or existing_app or
            db_exists or user_exists or
            user_data_folder_exists):
        raise forms.ValidationError(
            ('The username %(value)s is not available.'),
            params={'value': value},
        )
    return True


def validate_against_blacklist(username):
    if username.lower() in [x.lower() for x in settings.BLACKLISTED_USERNAMES]:
        raise forms.ValidationError(
            "The username '%s' is reserved for DataHub use." % (username)
        )

    return True


def validate_unique_email(value):
    try:
        User.objects.get(email=value.lower())
        raise forms.ValidationError(
            ("The email address %(value)s is in use by another account."),
            params={'value': value},
        )
    except User.DoesNotExist:
        return True


class UsernameForm(forms.Form):
    """
    A form that asks for a username and email address.

    Used by social auth flows, which authenticate new users before they've had
    a chance to provide that info.
    """

    invalid_username_msg = (
        "Usernames may only contain alphanumeric characters and "
        "underscores, and must not begin or end with an underscore."
    )
    regex = r'^(?![\_])[\w\_]+(?<![\_])$'
    validate_username = RegexValidator(regex, invalid_username_msg)

    username = forms.CharField(
        label="DataHub username",
        min_length=3,
        max_length=255,
        validators=[validate_username, validate_unique_username,
                    validate_against_blacklist])
    email = forms.EmailField(
        label="Email address",
        max_length=255,
        validators=[validate_unique_email])


class RegistrationForm(UsernameForm):
    """
    A form that asks for a username, email address, and password.

    Used for creating new users. The rendered template includes social auth
    registration links, which circumvent this form and lead to the social
    pipeline and UsernameForm.
    """

    password = forms.CharField(label=("Password"),
                               widget=forms.PasswordInput)


class LoginForm(forms.Form):
    """
    A form that asks for either a username or email address plus a password.

    Used to log in existing users. The rendered template includes social auth
    login links.
    """

    # `username` could be a username or email address, so be lax validating it.
    username = forms.CharField(label="Username or email address")
    password = forms.CharField(label=("Password"),
                               widget=forms.PasswordInput)


class EmailUniqueOrSameValidator(object):
    def __init__(self, old_email):
        self.old_email = old_email

    def __call__(self, value):
        if value == self.old_email:
            return True
        else:
            return validate_unique_email(value)


class ChangeEmailForm(forms.Form):
    """
    A form that asks for an email address.

    Used to change a logged in user's email address. The address must be a
    valid email address and either unique across users or the same as the
    current user's address. Forms can't tell who's logged in, so that must be
    checked in the view using this form.
    """

    def __init__(self, *args, **kwargs):
        old_email = kwargs.pop('old_email')
        super(ChangeEmailForm, self).__init__(*args, **kwargs)
        self.fields['email'] = forms.EmailField(
            label="Email address",
            max_length=255,
            required=True,
            validators=[EmailUniqueOrSameValidator(old_email)]
        )


class AddPasswordForm(forms.Form):

    password = forms.CharField(label=("Password"),
                               widget=forms.PasswordInput)
    password_confirm = forms.CharField(label=("Confirm Password"),
                                       widget=forms.PasswordInput)

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError(
                "The two password fields didn't match.")
        return password_confirm


class ForgotPasswordForm(PasswordResetForm):
    """
    A form that asks for an email address to send a password reset link to.

    Validates that the provided email is associated with an existing account
    and that the account has a password to reset. Social logins do not have a
    password to reset in DataHub.
    """

    def validate_resettable_email(value):
        try:
            user = User.objects.get(email=value.lower())
        except User.DoesNotExist:
            raise forms.ValidationError(
                ("No account found for %(value)s."),
                params={'value': value},
            )
        if user.has_usable_password():
            return True
        else:
            raise forms.ValidationError(
                ("%(value)s is a passwordless account. Please log in with its "
                 "associated identity provider."),
                params={'value': value},
                )

    email = forms.CharField(
        label="Email address",
        max_length=255,
        validators=[validate_resettable_email])

    class Meta:
        model = User
        fields = ('email',)
