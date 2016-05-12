class PermissionDenied(Exception):
    def __init__(self, *args, **kwargs):
        if not args:
            args = ('Access denied. Missing required privileges.',)
        Exception.__init__(self, *args, **kwargs)
