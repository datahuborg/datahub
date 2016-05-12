from psycopg2 import Error as PGError
from core.db.manager import PermissionDenied
from django.core.exceptions import ValidationError, \
                                   ObjectDoesNotExist
from django.template.context import RequestContext
from django.shortcuts import render_to_response


class DataHubManagerExceptionHandler(object):
    """docstring for DataHubManagerExceptionHandler"""

    def process_exception(self, request, exception):
        # Use an appropriate status code for each exception type.
        exceptions_by_status = {
            400: [
                ValueError,
                ValidationError,
                PGError,
            ],
            403: [
                PermissionDenied
            ],
            404: [
                ObjectDoesNotExist,
                LookupError
            ],
        }
        names_by_status = {
            400: "Bad Request",
            403: "Not Authorized",
            404: "Resource Not Found",
            500: "Internal Server Error"
        }
        # Default to a 500 error. If we can't explain what happened, blame
        # ourselves.
        status_code = 500
        for code, exceptions in exceptions_by_status.iteritems():
            if next((code for e in exceptions
                    if issubclass(type(exception), e)), None):
                status_code = code
                break

        context = RequestContext(request, {
            'status': status_code,
            'name': names_by_status[status_code],
            'error_type': type(exception).__name__,
            'detail': exception.message,
            })
        # Add extra info for psycopg errors
        if issubclass(type(exception), PGError):
            context['pgcode'] = exception.pgcode
            context['severity'] = exception.diag.severity

        return render_to_response(
            'exception.html', context,
            status=status_code)


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
