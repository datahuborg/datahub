from django import forms
from django.contrib.auth.models import User
from inventory.models import App
from core.db.manager import DataHubManager
from django.core.validators import RegexValidator


class UsernameForm(forms.Form):

    """
    A form that asks for a username and email address.

    Used by social auth flows, which authenticate new users before they've had
    a chance to provide that info.
    """

    invalid_username_msg = (
        "Usernames may only contain alphanumeric characters, hyphens, and "
        "underscores, and must not begin or end with an a hyphen or "
        "underscore."
        )
    regex = r'^(?![\-\_])[\w\-\_]+(?<![\-\_])$'
    validate_username = RegexValidator(regex, invalid_username_msg)

    def validate_unique_username(value):
        username = value.lower()
        try:
            User.objects.get(username=username)
            raise forms.ValidationError(
                ('The username %(value)s is not available.'),
                params={'value': value},
            )
        except User.DoesNotExist:
            pass

        try:
            App.objects.get(app_id=username)
            raise forms.ValidationError(
                ('The username %(value)s is not available.'),
                params={'value': value},
            )
        except App.DoesNotExist:
            pass

        db_exists = DataHubManager.database_exists(username)
        user_exists = DataHubManager.user_exists(username)
        if db_exists or user_exists:
            raise forms.ValidationError(
                ('The username %(value)s is not available.'),
                params={'value': value},
            )
        return True

    def validate_unique_email(value):
        try:
            User.objects.get(email=value.lower())
            raise forms.ValidationError(
                ('The email address %(value)s is in use by another account.'),
                params={'value': value},
            )
        except User.DoesNotExist:
            return True

    username = forms.CharField(
        label='DataHub Username',
        min_length=3,
        max_length=255,
        validators=[validate_username, validate_unique_username])
    email = forms.EmailField(
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
    username = forms.CharField()
    password = forms.CharField(label=("Password"),
                               widget=forms.PasswordInput)
