bind = "0.0.0.0:8000"
workers = 5
daemon = False
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"
