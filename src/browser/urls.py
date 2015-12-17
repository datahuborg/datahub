from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView
from account import forms as account_forms


urlpatterns = patterns(
    '',

    # Home Page
    url(r'^$', 'browser.views.home'),
    url(r'^about$', 'browser.views.about'),  # for backward compatibility
    url(r'^favicon\.ico$',
        RedirectView.as_view(url='/static/images/favicon.ico',
                             permanent=True)),

    # WWW Pages
    url(r'^www/', include('www.urls')),

    # Account Related
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^account/login/$', 'account.views.login', name='login'),
    url(r'^account/register/$', 'account.views.register', name='register'),
    url(r'^home/$', 'account.views.home'),
    url(r'^account/logout/$', 'account.views.logout', name='logout'),
    url(r'^account/choose_username/$', 'account.views.get_user_details'),
    # Use Django's built-in password reset tools.
    url(r'^account/forgot/$', 'django.contrib.auth.views.password_reset',
        {
            'template_name': 'forgot.html',
            'email_template_name': 'password_reset_email.html',
            'subject_template_name': 'password_reset_subject.txt',
            'password_reset_form': account_forms.ForgotPasswordForm,
            'from_email': 'noreply@datahub.csail.mit.edu',
        },
        name='password_reset'),
    url(r'^account/forgot/done/$',
        'django.contrib.auth.views.password_reset_done',
        {
            'template_name': 'forgot-done.html',
        },
        name='password_reset_done'),
    url((r'^account/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/' \
         r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$'),
        'django.contrib.auth.views.password_reset_confirm',
        name='password_reset_confirm'),
    url(r'^account/reset/done/$',
        'django.contrib.auth.views.password_reset_complete',
        name='password_reset_complete'),
    url(r'^account/reset/$', 'account.views.reset_password'),
    url(r'^account/verify/$', 'account.views.verify_email'),


    # Thrift Services
    url(r'^service$', 'browser.views.service_core_binary'),
    url(r'^service/account$', 'browser.views.service_account_binary'),
    url(r'^service/json$', 'browser.views.service_core_json'),

    # Create
    url(r'^create/(\w+)/repo/?$', 'browser.views.repo_create'),

    url(r'^create/(\w+)/(\w+)/card/?$', 'browser.views.card_create'),

    url(r'^create/annotation/?$', 'browser.views.create_annotation'),


    # Browse
    url(r'^browse/(\w+)/(\w+)/table/(\w+)/?$', 'browser.views.table'),

    url(r'^browse/(\w+)/(\w+)/query/?$', 'browser.views.query'),

    url(r'^browse/(\w+)/(\w+)/card/(.+)/?$', 'browser.views.card'),

    url(r'^browse/(\w+)/(\w+)/?$', 'browser.views.repo'),

    url(r'^browse/(\w+)/(\w+)/tables/?$', 'browser.views.repo_tables'),

    url(r'^browse/(\w+)/(\w+)/files/?$', 'browser.views.repo_files'),

    url(r'^browse/(\w+)/(\w+)/cards/?$', 'browser.views.repo_cards'),

    url(r'^browse/(\w+)/?$', 'browser.views.user'),


    # Delete
    url(r'^delete/(\w+)/(\w+)/?$', 'browser.views.repo_delete'),

    url(r'^delete/(\w+)/(\w+)/table/(\w+)/?$', 'browser.views.table_delete'),

    url(r'^delete/(\w+)/(\w+)/card/(\w+)/?$', 'browser.views.card_delete'),

    url(r'^delete/(\w+)/(\w+)/file/([ -~]+)/?$', 'browser.views.file_delete'),


    # Export
    url(r'^export/(\w+)/(\w+)/table/(\w+)/?$', 'browser.views.table_export'),
    url(r'^export/(\w+)/(\w+)/card/(\w+)/?$', 'browser.views.card_export'),


    # Special File Operations
    url(r'^upload/(\w+)/(\w+)/file/?$', 'browser.views.file_upload'),
    url(r'^import/(\w+)/(\w+)/file/([ -~]+)', 'browser.views.file_import'),
    url(r'^download/(\w+)/(\w+)/file/([ -~]+)', 'browser.views.file_download'),


    # Settings
    url(r'^settings/(\w+)/(\w+)/?$', 'browser.views.repo_settings'),


    # Collaborators
    url(r'^collaborator/repo/(\w+)/(\w+)/add/?$',
        'browser.views.repo_collaborators_add'),

    url(r'^collaborator/repo/(\w+)/(\w+)/remove/(\w+)/?$',
        'browser.views.repo_collaborators_remove'),

    # Developer Apps
    url(r'^developer/apps/?$', 'browser.views.apps'),

    url(r'^developer/apps/register/?$', 'browser.views.app_register'),

    url(r'^developer/apps/remove/(\w+)/?$', 'browser.views.app_remove'),

    # Permissions
    url(r'^permissions/apps/allow_access/(\w+)/(\w+)$',
        'browser.views.app_allow_access'),


    # Client Apps
    url(r'^apps/console/', include('console.urls')),
    url(r'^apps/refiner/', include('refiner.urls')),
    url(r'^apps/dbwipes/', include('dbwipes.urls')),
    url(r'^apps/viz/', include('viz2.urls')),
    url(r'^apps/sentiment/', include('sentiment.urls')),
    url(r'^apps/dataq/', include('dataq.urls')),
    url(r'^apps/datatables/', include('datatables.urls')),
)
