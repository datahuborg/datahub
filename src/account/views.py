from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect, render
from django import forms
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from social.backends.utils import load_backends
from operator import itemgetter

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
    # return render(request, 'login.html')


class UsernameField(forms.CharField):
    def validate(self, value):
        """Check if the username is already in use."""
        try:
            User.objects.get(username=value)
            raise forms.ValidationError(
                ('The username %(value)s is already in use.'),
                params={'value': value},
            )
        except User.DoesNotExist:
            return True


class UsernameForm(forms.Form):
    preferred_username = UsernameField(max_length=255)


def get_username(request):
    if request.method == 'POST':
        form = UsernameForm(request.POST)
        if form.is_valid():
            # because of FIELDS_STORED_IN_SESSION, this will get copied
            # to the request dictionary when the pipeline is resumed
            request.session['preferred_username'] = form.cleaned_data['preferred_username']

            # once we have the password stashed in the session, we can
            # tell the pipeline to resume by using the "complete" endpoint
            backend = request.session['partial_pipeline']['backend']
            return redirect('social:complete', backend=backend)
    else:
        form = UsernameForm()

    return render(request, "registration/username_form.html", {'form': form})


@login_required(login_url='/')
def home(request):
    return render_to_response('home.html')


def logout(request):
    auth_logout(request)
    return redirect('/')
