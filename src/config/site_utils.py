from django.contrib.sites.models import Site
from django.db.utils import ProgrammingError


def set_site_info(domain='datahub-local.mit.edu', name='MIT DataHub'):
    try:
        site = Site.objects.get_current()
        if site.domain != domain:
            site.domain = domain
            site.name = name
            site.save()
    except ProgrammingError:
        pass
