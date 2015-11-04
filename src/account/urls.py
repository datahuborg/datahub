from django.conf.urls import patterns, include, url
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.dispatch import receiver
from registration.signals import user_registered

@receiver(user_registered)
def registration_callback(sender, **kwargs):
    # Create the user's repo and give them a Postgres user here

urlpatterns = patterns(
    '',
    # url(r'^', include('registration.backends.simple.urls')),
    # url('^register', CreateView.as_view(
    #         template_name='registration/register.html',
    #         form_class=UserCreationForm,
    #         success_url='/'
    # )),
    # url(r'^', include('django.contrib.auth.urls')),
    # url(r'^old/login', 'account.auth.login'),
    # url(r'^old/register', 'account.auth.register'),
    # url(r'^old/logout', 'account.auth.logout'),

    # url(r'^old/forgot', 'account.auth.forgot'),
    # url(r'^old/jdbc_password', 'account.auth.jdbc_password'),
    # url(r'^old/reset/(\w+)', 'account.auth.reset'),
    # url(r'^old/verify/(\w+)', 'account.auth.verify'),
    # url(r'^old/settings', 'account.auth.account_settings'),
    # url(r'^old/add_login', 'account.auth.add_login'),
    # url(r'^old/confirm_add_login', 'account.auth.confirm_add_login'),
)
