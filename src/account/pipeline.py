from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from social.pipeline.partial import partial
from account.views import add_password


@partial
def get_user_details(strategy, details, is_new=False, *args, **kwargs):
    """Asks new users to choose a username and verify their email address."""
    if is_new:
        # request['preferred_username'] is set by the pipeline infrastructure
        # because it is whitelisted in FIELDS_STORED_IN_SESSION and is set by
        # accounts.views.get_user_details.
        preferred_username = strategy.session.get('preferred_username', None)
        email = strategy.session.get('email', None)
        if not preferred_username:
            # If we return something besides a dict or None, then Python
            # Social Auth return it to the user. In this case we return a
            # redirect response to a view that asks the user to choose a
            # username and provide and email address.
            return redirect(reverse("account.views.get_user_details"))

        result = {
            'username': preferred_username,
            'email': email,
        }
        return result
    else:
        return None


@partial
def set_password_if_needed(strategy, user, *args, **kwargs):
    """Requires disconnecting users to have at least one login method."""
    if not user.has_usable_password() and user.social_auth.count() == 1:
        return add_password(strategy.request, is_disconnect=True)
    else:
        return None
