from django.conf import settings
from django.shortcuts import render_to_response, redirect, render
from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth import logout as django_logout, \
                                login as django_login, \
                                authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from social.backends.utils import load_backends
from operator import itemgetter
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db.utils import IntegrityError


def provider_details():
    # For templates. Intersect with settings.AUTHENTICATION_BACKENDS to limit
    # to enabled social backends.
    #
    # `backend` is the backend name Python Social Auth understands.
    # `name` is the display name to be shown in templates.
    # `icon` is the id of the Font Awesome icon matching the backend.
    # `priority` is the sort order. Lower numbers sort first.
    providers = [
        {
            'backend': 'google-oauth2',
            'name': 'Google',
            'icon': 'google',
            'priority': -90,
        },
        {
            'backend': 'twitter',
            'name': 'Twitter',
            'icon': 'twitter',
            'priority': 0,
        },
        {
            'backend': 'reddit',
            'name': 'Reddit',
            'icon': 'reddit',
            'priority': 0,
        },
        {
            'backend': 'steam',
            'name': 'Steam',
            'icon': 'steam',
            'priority': 0,
        },
        {
            'backend': 'facebook',
            'name': 'Facebook',
            'icon': 'facebook',
            'priority': -80,
        },
        {
            'backend': 'flickr',
            'name': 'Flickr',
            'icon': 'flickr',
            'priority': 0,
        },
        {
            'backend': 'github',
            'name': 'GitHub',
            'icon': 'github',
            'priority': 0,
        },
        {
            'backend': 'twitch',
            'name': 'Twitch',
            'icon': 'twitch',
            'priority': 0,
        },
        {
            'backend': 'mit-oidc',
            'name': 'MIT OpenID Connect',
            'icon': 'mit',
            'priority': -1000,
        },
    ]

    enabled_backends = load_backends(settings.AUTHENTICATION_BACKENDS)

    providers = [p for p in providers if p['backend'] in enabled_backends]
    providers = sorted(providers, key=itemgetter('priority', 'name'))
    return providers


def login(request):
    """
    DataHub account login form.

    GET returns and HttpResponse containing the account login form.
    POST logs in name/email/password accounts.
    Other links from the page lead to Python Social Auth options (Google,
    Facebook, Twitter, etc).
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # If username looks like an email address, look up the username
            # associated with that address.
            #
            # The username regex disallows the @ symbol, and the email regex
            # requires it.
            if '@' in username:
                try:
                    user = User.objects.get(email=username)
                    username = user.username
                except User.DoesNotExist:
                    user = None
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                django_login(request, user)
            else:
                form.add_error(None, "Username and password do not match.")
        else:
            # Form isn't valid. Fall through to return it to the user with
            # errors.
            pass
    else:
        form = LoginForm()

    providers = provider_details()
    context = RequestContext(request, {
        'request': request,
        'user': request.user,
        'form': form,
        'providers': providers})
    return render_to_response('login.html', context_instance=context)


def register(request):
    """
    DataHub account registration form.

    GET returns an HttpResponse containing the account registration form.
    POST creates a name/email/password account and logs the new user in.
    Other links from the page lead to Python Social Auth options (Google,
    Facebook, Twitter, etc).
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            User.objects.create_user(username, email, password)
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                django_login(request, user)
                return redirect('/')
        else:
            # Form isn't valid. Fall through to return it to the user with
            # errors.
            pass
    else:
        form = RegistrationForm()

    providers = provider_details()
    context = RequestContext(request, {
        'request': request,
        'user': request.user,
        'form': form,
        'providers': providers})
    return render_to_response('register.html', context_instance=context)


#
# Should move this to a separate signals.py, register it in a ready() method,
# and leave a note here that email uniqueness is enforced by a pre_save signal
# handler on the User model.
@receiver(pre_save, sender=User, dispatch_uid="dh_unique_username")
def user_pre_save(sender, instance=None, **kwargs):
    """
    Validates new user attributes at database save time. beyond the User model's rules.

    Check here in validation and in the pipeline at create_user that the provided email address is already in use, 
    """
    email = instance.email
    username = instance.username
    if not email:
        raise IntegrityError("Email required.")
    if sender.objects.filter(email=email).exclude(username=username).count():
        raise IntegrityError(
            "The email address {0} is in use by another account.".format(email))


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
        try:
            User.objects.get(username=value)
            raise forms.ValidationError(
                ('The username %(value)s is not available.'),
                params={'value': value},
            )
        except User.DoesNotExist:
            return True

    def validate_unique_email(value):
        try:
            User.objects.get(email=value)
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


# Called by the get_username pipeline. Look for pipeline.py and the
# SOCIAL_AUTH_PIPELINE section of settings.py.
def get_username(request):
    # Prepopulate the form with values provided by the identity provider.
    pipeline_args = request.session['partial_pipeline']['kwargs']
    backend = request.session['partial_pipeline']['backend']
    try:
        details = pipeline_args['details']
    except KeyError:
        details = None
    try:
        # Include details about the social login being used,
        # e.g. "Authenticated as Facebook user FooBar."
        providers = provider_details()
        provider = next((p for p in providers if p['backend'] == backend), None)
        social = {
            'username': pipeline_args['username'],
            'name': provider['name'],
            'icon': provider['icon'],
        }
    except KeyError:
        social = None

    if request.method == 'POST':
        form = UsernameForm(request.POST)
        if form.is_valid():
            # Because of FIELDS_STORED_IN_SESSION, preferred_username will be
            # copied to the request dictionary when the pipeline resumes.
            d = {
                'preferred_username': form.cleaned_data['username'],
                'email': form.cleaned_data['email'],
            }
            request.session.update(d)

            # Once we have the password stashed in the session, we can
            # tell the pipeline to resume by using the "complete" endpoint
            return redirect('social:complete', backend=backend)
    else:
        form = UsernameForm(initial={'email': details['email']})

    context = RequestContext(request, {
        'form': form,
        'details': details,
        'social': social
        })

    return render(request, "registration/username_form.html",
                  context)


@login_required(login_url='/')
def home(request):
    return render_to_response('home.html')


def logout(request):
    django_logout(request)
    return redirect('/')
