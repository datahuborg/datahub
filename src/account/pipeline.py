from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from social.pipeline.partial import partial


@partial
def get_username(strategy, details, is_new=False, *args, **kwargs):
    if is_new:
        # request['preferred_username'] is set by the pipeline infrastructure
        # because it exists in FIELDS_STORED_IN_SESSION.
        preferred_username = strategy.session.get('preferred_username', None)
        if not preferred_username:

            # if we return something besides a dict or None, then that is
            # returned to the user -- in this case we will return a redirect to a
            # view that can be used to get a password.
            return redirect(reverse("account.views.get_username"))

        # grab the user object from the database (remember that they may
        # not be logged in yet) and set their password.  (Assumes that the
        # email address was captured in an earlier step.)
        result = {'username': preferred_username}
        return result
    else:
        return None
