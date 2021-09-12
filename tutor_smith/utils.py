from .converters import h_decode, user_hasher
from user_management.models import User

# TODO: Write functional Ipgrabber eg. with django-ipware
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    elif request.META.get('HTTP_X_REAL_IP'):
        ip = request.META.get('HTTP_X_REAL_IP')
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def is_user_authenticated(request) -> User:
    try:
        id = request.session['userid']
    except KeyError:
        return None
    if id:
        id = h_decode(user_hasher, request.session['userid'])
    try:
        return User.objects.get(id=id)
        '''
        if not user.ip == get_client_ip(request):
            return None
        '''
    except User.DoesNotExist:
        pass
    return None
