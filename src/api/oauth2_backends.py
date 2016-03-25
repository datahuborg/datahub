from oauth2_provider.oauth2_backends import OAuthLibCore

import json


class ContentNegotiatingOAuthLibCore(OAuthLibCore):
    """
    Extends the default OAuthLibCore to handle both JSON and form POSTs.

    Parses requests with application/json and form/www-url-encoded Content-Type
    """

    def extract_body(self, request):
        if ('CONTENT_TYPE' in request.META and
                request.META['CONTENT_TYPE'] == 'application/json'):
            try:
                body = json.loads(request.body.decode('utf-8')).items()
            except ValueError:
                body = ""
            return body
        return request.POST.items()
