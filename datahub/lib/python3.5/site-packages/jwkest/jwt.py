import json
from jwkest import b64d
from jwkest import b64e
from jwkest import BadSyntax

__author__ = 'roland'


def split_token(token):
    if not token.count(b"."):
        raise BadSyntax(token,
                        "expected token to contain at least one dot")
    return tuple(token.split(b"."))


def b2s_conv(item):
    if isinstance(item, bytes):
        return item.decode("utf-8")
    elif isinstance(item, (str, int, bool)):
        return item
    elif isinstance(item, list):
        return [b2s_conv(i) for i in item]
    elif isinstance(item, dict):
        return dict([(k, b2s_conv(v)) for k, v in item.items()])


def b64encode_item(item):
    if isinstance(item, bytes):
        return b64e(item)
    elif isinstance(item, str):
        return b64e(item.encode("utf-8"))
    elif isinstance(item, int):
        return b64e(item)
    else:
        return b64e(json.dumps(b2s_conv(item),
                               separators=(",", ":")).encode("utf-8"))


class JWT(object):
    def __init__(self, **headers):
        self.headers = headers
        self.part = []
        self.b64part = []

    def unpack(self, token):
        """
        Unpacks a JWT into its parts and base64 decodes the parts
        individually

        :param token: The JWT
        """
        if isinstance(token, str):
            token = token.encode("utf-8")

        part = split_token(token)
        self.b64part = part
        self.part = [b64d(p) for p in part]
        self.headers = json.loads(self.part[0].decode("utf-8"))
        return self

    def pack(self, parts, headers=None):
        """
        Packs components into a JWT

        :param returns: The string representation of a JWT
        """
        if not headers:
            if self.headers:
                headers = self.headers
            else:
                headers = {'alg': 'none'}

        _all = [b64encode_item(headers)]
        _all.extend([b64encode_item(p) for p in parts])

        return b".".join(_all)

    def payload(self):
        _msg = self.part[1].decode("utf-8")

        # If not JSON web token assume JSON
        if "cty" in self.headers and self.headers["cty"].lower() != "jwt":
            pass
        else:
            try:
                _msg = json.loads(_msg)
            except ValueError:
                pass

        return _msg