from hashids import Hashids
from django.conf import settings

user_min_length = 8
reset_min_length = 12

"""
Use these hashers for parameters in the decode / encode method
"""
user_hasher = Hashids(settings.HASHIDS_SALT, min_length=user_min_length)
reset_hasher = Hashids(
    settings.RESET_HASHIDS_SALT, min_length=reset_min_length
)

# IDEA: Move this into utils
def h_encode(hasher: Hashids, *args) -> str:
    """
    This function converts an intiger to an hashed id.
    This function requires a hasher
    """
    return hasher.encode(*args)


def h_decode(hasher: Hashids, h: str) -> int:
    """
    This function converts a hashed id into an intiger.
    This function requires a hasher
    """
    z = hasher.decode(h)
    if z:
        return z[0]


def h_m_decode(hasher: Hashids, h: str) -> tuple:
    """
    This function converts a hashed id into an tuple.
    This function requires a hasher
    """
    z = hasher.decode(h)
    if z:
        return z


class UserHashIdConverter:
    """
    This converter is only for urls.py Don't use this for getting Hashids
    """

    regex = f'[a-zA-Z0-9]{{{user_min_length},}}'

    def to_python(self, value):
        return h_decode(user_hasher, value)

    def to_url(self, value):
        return h_encode(user_hasher, value)


class MultipleHashIdConverter:
    """
    This converter is only for urls.py Don't use this for getting Hashids
    """

    regex = f'[a-zA-Z0-9]{{{user_min_length},}}'

    def to_python(self, value):
        return h_m_decode(user_hasher, value)

    def to_url(self, value):
        return h_encode(user_hasher, value)


class ResetHashIdConverter:
    """
    This converter is only for urls.py Don't use this for getting Hashids
    """

    regex = f'[a-zA-Z0-9]{{{reset_min_length},}}'

    def to_python(self, value):
        return h_decode(reset_hasher, value)

    def to_url(self, value):
        return h_encode(reset_hasher, value)
