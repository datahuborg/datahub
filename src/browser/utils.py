import hashlib
import re
import urllib
import urlparse
from Crypto.Cipher import AES
from Crypto import Random

kKey = 'datahub'


def encrypt_text(plain_text):
    key = hashlib.sha256(kKey).digest()
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    crypt_text = (iv + cipher.encrypt(plain_text)).encode('hex')
    return crypt_text


def decrypt_text(crypt_text):
    iv_len = AES.block_size
    key = hashlib.sha256(kKey).digest()
    iv = crypt_text.decode('hex')[:iv_len]
    cipher = AES.new(key, AES.MODE_CFB, iv)
    plain_text = cipher.decrypt(crypt_text.decode('hex'))[iv_len:]
    return plain_text


def clean_str(text, prefix):
    s = text.strip().lower()

    # replace whitespace with '_'
    s = re.sub(' ', '_', s)

    # remove invalid characters
    s = re.sub('[^0-9a-zA-Z_]', '', s)

    # remove leading characters until a letter or underscore
    s = re.sub('^[^a-zA-Z_]+', '', s)

    if s == '':
        return clean_str(prefix + text, '')

    return s


def rename_duplicates(columns):
    columns = [c.lower() for c in columns]
    new_columns = []
    col_idx = {c: 1 for c in columns}

    for c in columns:
        if columns.count(c) == 1:
            new_columns.append(c)
        else:
            # add a suffix
            new_columns.append(c + str(col_idx[c]))
            col_idx[c] += 1

    return new_columns


def post_or_get(request, key, fallback=None):
    """
    Returns request param from GET and POST if available, fallback otherwise.

    Precedence is POST, GET, then fallback if not found.
    """
    return request.POST.get(key, request.GET.get(key, fallback))


def add_query_params_to_url(url, params):
    """
    Returns the given URL with the dictionary of params encoded and appended.

    Works for URLs with or without query parameters.
    """
    parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(parts[4]))
    query.update(params)
    parts[4] = urllib.urlencode(query)

    return urlparse.urlunparse(parts)
