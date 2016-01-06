from django import template

register = template.Library()


@register.filter(name='mapattr')
def mapattr(value, arg):
    """
    Maps an attribute from a list into a new list.

    e.g. value = [{'a': 1}, {'a': 2}, {'a': 3}]
         arg = 'a'
         result = [1, 2, 3]
    """
    if len(value) > 0:
        res = [getattr(o, arg) for o in value]
        return res
    else:
        return []


@register.filter(name='joinand')
def joinStrings(value):
    """
    Converts a list of strings into a single string with an oxford comma.

    e.g. ['a', 'b', 'c'] => "a, b, and c"
         ['a', 'b'] => "a and b"
         ['a'] => "a"
    """
    if len(value) > 2:
        value[-1] = str("and " + value[-1])
        return str(", ".join(value))
    elif len(value) == 2:
        return str(" and ".join(value))
    elif len(value) == 1:
        return value[0]
    else:
        return ''
