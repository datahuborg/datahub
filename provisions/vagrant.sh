# Add Docker apt repo gpg key
apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys \
    58118E89F3A912897C070ADBF76221572C52609D
echo "deb https://apt.dockerproject.org/repo ubuntu-trusty main" > \
    /etc/apt/sources.list.d/docker.list
apt-get update
apt-get install -y docker-engine

echo "Making a temporary self-signed certificate..."
echo "To use your own certificate, replace the contents of /ssl in this VM"
echo "and restart the \`web\` container."
mkdir /ssl
openssl req \
    -new \
    -newkey rsa:4096 \
    -days 365 \
    -nodes \
    -x509 \
    -subj "/C=US/ST=Massachusetts/L=Cambridge/O=MIT CSAIL/CN=datahub-local.mit.edu" \
    -keyout /ssl/nginx.key \
    -out /ssl/nginx.crt 2> /dev/null

cd /vagrant
sh provisions/docker/build-images.sh
sh provisions/docker/create-dev-containers.sh
