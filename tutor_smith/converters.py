from django.contrib.auth.hashers import reset_hashers
from hashids import Hashids
from django.conf import settings

user_min_length = 8
reset_min_length = 12

user_hasher = Hashids(settings.HASHIDS_SALT, min_length=user_min_length)
reset_hasher = Hashids(
    settings.RESET_HASHIDS_SALT, min_length=reset_min_length
)


def h_encode(hasher, id):
    return hasher.encode(id)


def h_decode(hasher, h):
    z = hasher.decode(h)
    if z:
        return z[0]


class UserHashIdConverter:
    regex = f'[a-zA-Z0-9]{{{user_min_length},}}'

    def to_python(self, value):
        return h_decode(user_hasher, value)

    def to_url(self, value):
        return h_encode(user_hasher, value)


class ResetHashIdConverter:
    regex = f'[a-zA-Z0-9]{{{reset_min_length},}}'

    def to_python(self, value):
        return h_decode(reset_hasher, value)

    def to_url(self, value):
        return h_encode(reset_hasher, value)
