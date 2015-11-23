from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect, render
from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth import logout as auth_logout
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
    providers = provider_details()
    context = RequestContext(request, {
        'request': request, 'user': request.user, 'providers': providers})
    return render_to_response('login.html', context_instance=context)

def register(request):
    providers = provider_details()
    context = RequestContext(request, {
        'request': request, 'user': request.user, 'providers': providers})
    return render_to_response('register.html', context_instance=context)


# Disallow emails that already exist, both here in validation and in the
# pipeline at create_user
#
# Should move this to a separate signals.py, register it in a ready() method,
# and leave a note here that email uniqueness is enforced by a pre_save signal
# handler on the User model.
@receiver(pre_save, sender=User, dispatch_uid="dh_unique_username")
def user_pre_save(sender, instance=None, **kwargs):
    email = instance.email
    username = instance.username
    print "About to save user {0} with email {1}.".format(username, email)
    if not email:
        raise IntegrityError("Email required.")
    if sender.objects.filter(email=email).exclude(username=username).count():
        raise IntegrityError("{0} is in use by another account.".format(email))


class UsernameForm(forms.Form):

    invalid_username_msg = 'Username may only contain alphanumeric characters, hyphens, and underscores, and must not begin or end with an a hypen or underscore.'
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

    preferred_username = forms.CharField(
        label='DataHub Username',
        min_length=3,
        max_length=255,
        validators=[validate_username, validate_unique_username])
    email = forms.EmailField(
        max_length=255,
        validators=[validate_unique_email])



# Called by the get_username pipeline. Look for pipeline.py and the
# SOCIAL_AUTH_PIPELINE section of settings.py.
def get_username(request):
    # Prepopulate the form with values provided by the identity provider.
    pipeline_args = request.session['partial_pipeline']['kwargs']
    try:
        details = pipeline_args['details']
    except (KeyError, AttributeError):
        details = None
    try:
        # Include details about the social login being used
        providers = provider_details()
        backend = request.session['partial_pipeline']['backend']
        provider = next((p for p in providers if p['backend'] == backend), None)
        social = {
            'username': pipeline_args['username'],
            'name': provider['name'],
            'icon': provider['icon'],
        }
    except (Exception), e:
        social = None

    if request.method == 'POST':
        form = UsernameForm(request.POST)
        if form.is_valid():
            # because of FIELDS_STORED_IN_SESSION, this will get copied
            # to the request dictionary when the pipeline is resumed
            request.session['preferred_username'] = form.cleaned_data['preferred_username']
            request.session['email'] = form.cleaned_data['email']

            # once we have the password stashed in the session, we can
            # tell the pipeline to resume by using the "complete" endpoint
            backend = request.session['partial_pipeline']['backend']
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
    auth_logout(request)
    return redirect('/')
