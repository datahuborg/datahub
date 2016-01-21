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

# Make Docker scripts available in shell as dh-* commands.
for f in /vagrant/provisions/docker/*.sh; do
    ln -s $f /usr/local/sbin/dh-$(basename $f .sh);
done

source ~/.profile
dh-build-images
dh-create-dev-containers

if [ ! -f src/config/secret_key.py ]; then
    echo "No Django SECRET_KEY found, generating a new one..."
    docker run --rm --volumes-from app datahuborg/datahub /bin/bash -c "python src/scripts/generate_secret_key.py"
    echo "Done."
fi
