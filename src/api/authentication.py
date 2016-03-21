from rest_framework.authentication import SessionAuthentication


class CSRF_Exempt(SessionAuthentication):

    def enforce_csrf(self, request):
        return
