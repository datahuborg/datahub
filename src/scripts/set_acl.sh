#!/bin/sh
# mkfs -t ext4 /dev/disk/by-id/virtio-xxx
# mkdir /user_data
# mount /dev/disk/by-id/virtio-xxx /user_data
chown -R www-data:www-data /user_data/
chmod -R 3775 /user_data/
setfacl -d -R -m g:www-data:rwx /user_data
setfacl -d -R -m g:postgres:rwx /user_data
setfacl -d -R -m g:postgres:rwx /user_data
