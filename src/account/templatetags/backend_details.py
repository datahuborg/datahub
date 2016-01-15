from django import template
from account.utils import provider_details

register = template.Library()


def get_provider_attr(backend=None, attr=None):
    try:
        return provider_details(backend)[attr]
    except TypeError:
        return ''


@register.filter(name='provider_name')
def provider_name_filter(value):
    """
    Returns the display name for a Python Social Auth backend.

    e.g., given 'google-oauth2' this will return "Google".
    Invalid backends are returned as ''.
    """
    return get_provider_attr(value, attr='name')


@register.filter(name='provider_names')
def provider_names_filter(value):
    """
    Returns the display names for a list of Python Social Auth backends.

    e.g., given ['google-oauth2', 'twitter'] this will return
          ["Google", "Twitter"].
    Invalid backends are returned as ''.
    """
    return [get_provider_attr(backend, attr='name') for backend in value]


@register.filter(name='provider_icon')
def provider_icon_filter(value):
    """
    Returns the icon CSS class for a Python Social Auth backend.

    e.g., given "google-oauth2" this will return "fa-google".
    Invalid backends are returned as ''.
    """
    return get_provider_attr(value, attr='icon')
