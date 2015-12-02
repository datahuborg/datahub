from django.conf import settings
from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import logout as django_logout, \
                                login as django_login, \
                                authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from social.backends.utils import load_backends
from operator import itemgetter
import forms


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
            'icon': 'steam-square',
            'priority': 0,
        },
        {
            'backend': 'facebook',
            'name': 'Facebook',
            'icon': 'facebook-official',
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
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # If username looks like an email address, look up the username
            # associated with that address.
            #
            # This assumes the username regex disallows the @ symbol, and the
            # email regex requires it.
            if '@' in username:
                try:
                    user = User.objects.get(email=username)
                    username = user.username
                except User.DoesNotExist:
                    user = None
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                django_login(request, user)
                return redirect('/')
            else:
                form.add_error(None, "Username and password do not match.")
        else:
            # Form isn't valid. Fall through to return it to the user with
            # errors.
            pass
    else:
        form = forms.LoginForm()

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
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            User.objects.create_user(username, email, password)
            # A signal handler in signals.py listens for the pre_save signal
            # and throws an IntegrityError if the user's email address is not
            # unique. Username uniqueness is handled by the model.
            #
            # In the future, another pre_save signal handler will check if a
            # DataHub database exists for the user and create one if it
            # doesn't exist. If the database cannot be create, that handler
            # will throw an exception.
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                django_login(request, user)
                return redirect('/')
        else:
            # Form isn't valid. Fall through to return it to the user with
            # errors.
            pass
    else:
        form = forms.RegistrationForm()

    providers = provider_details()
    context = RequestContext(request, {
        'request': request,
        'user': request.user,
        'form': form,
        'providers': providers})
    return render_to_response('register.html', context_instance=context)


# Called by the get_user_details pipeline. Look for pipeline.py and the
# SOCIAL_AUTH_PIPELINE section of settings.py.
def get_user_details(request):
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
            'username': details['username'],
            'name': provider['name'],
            'icon': provider['icon'],
        }
    except KeyError:
        social = None

    if request.method == 'POST':
        form = forms.UsernameForm(request.POST)
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
        form = forms.UsernameForm(initial={'email': details['email']})

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
