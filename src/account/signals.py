from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db.utils import IntegrityError


# Note that this may fire multiple times and for users that already exist.
@receiver(pre_save, sender=User, dispatch_uid="dh_user_pre_save_unique_email")
def user_pre_save(sender, instance=None, **kwargs):
    """
    Validates new user attributes at database save time.

    Check is made both here and in the pipeline form to ensure the provided
    email address is not being used by another user.
    """
    email = instance.email
    username = instance.username
    if not email:
        raise IntegrityError("Email required.")
    if sender.objects.filter(email=email).exclude(username=username).count():
        raise IntegrityError(
            "The email address {0} is associated with another account."
            .format(email)
        )
