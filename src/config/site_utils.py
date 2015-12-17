from django.contrib.sites.models import Site


def set_site_info(domain='datahub-local.mit.edu', name='MIT DataHub'):
    site = Site.objects.get_current()
    if site.domain != domain:
        site.domain = domain
        site.name = name
        site.save()
