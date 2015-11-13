file='/var/lib/postgresql/data/postgresql.conf'
marker="DATAHUB CUSTOM SETTINGS"
settings="
log_statement = 'all'
log_destination = 'stderr'
logging_collector = on
log_directory = '/var/log/postgresql'
log_truncate_on_rotation = on
log_rotation_age = 1d
"

if ! grep -q "${marker}" "${file}" ; then
    echo "******ENABLING POSTGRESQL LOGGING******"
    echo "#------------------------------------------------------------------------------" >> "${file}"
    echo "# ${marker}" >> "${file}"
    echo "#------------------------------------------------------------------------------" >> "${file}"
    echo "${settings}" >> "${file}"
    sed -i -e"s/^#listen_addresses =.*$/listen_addresses = 'localhost'/" "${file}"
fi
