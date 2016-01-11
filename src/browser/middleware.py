# Credit to @mattrobenolt:
# - https://mattrobenolt.com/handle-x-forwarded-port-header-in-django/
#
# This will be unnecessary once DataHub is on Django 1.9.
# - https://code.djangoproject.com/ticket/25211


class XForwardedPort(object):
    def process_request(self, request):
        try:
            request.META['SERVER_PORT'] = request.META['HTTP_X_FORWARDED_PORT']
        except KeyError:
            pass
        return None
