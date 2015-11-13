FROM nginx:1.9.5
# The base nginx images symlinks the logs to stdout and stderr,
# but we want them to go to disk.
RUN rm /var/log/nginx/access.log /var/log/nginx/error.log
COPY nginx.conf /etc/nginx/nginx.conf
COPY default.conf /etc/nginx/conf.d/default.conf
RUN mkdir -p /etc/nginx/ssl
