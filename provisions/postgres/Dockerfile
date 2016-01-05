FROM postgres:9.4.5

ENV DB_NAME datahub
ENV DB_USER postgres
ADD 00_create_database_if_not_exists.sh /docker-entrypoint-initdb.d/
ADD 01_enable_postgres_logging.sh /docker-entrypoint-initdb.d/
ADD 02_set_user_data_permissions.sh /docker-entrypoint-initdb.d/
VOLUME /user_data
