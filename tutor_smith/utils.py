from typing import List
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models.query import QuerySet
from django.http.response import Http404
from .converters import h_decode, user_hasher
from user_management.models import User

# TODO: Write functional Ipgrabber eg. with django-ipware
def get_client_ip(request):
    """
    Returns an ip
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    elif request.META.get('HTTP_X_REAL_IP'):
        ip = request.META.get('HTTP_X_REAL_IP')
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def is_user_authenticated(request, force_authentication=False) -> User:
    """
    returns a user if the user exists and if he is authenticated
    """
    try:
        id = request.session['userid']
    except KeyError:
        if force_authentication:
            raise PermissionDenied('User needs to be authenticated')
        else:
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
    if force_authentication:
        raise PermissionDenied('User needs to be authenticated')
    else:
        return None


def display_messages(request, msg, msg_type: int) -> None:
    """
    A simple Function for diplaying one or more messages with the Django messages API
    msg_type is e.g messages.ERROR or messages.SUCCESS
    """
    if type(msg) == List:
        for err in msg:
            messages.add_message(request, msg_type, err)
    else:
        messages.add_message(request, msg_type, msg)


def get_set_or_404(object, *args, **kwargs) -> QuerySet:
    """
    Returns a QuerySet or 404 if it does't exist.
    Similar to get_object_or_404
    kwargs are used for querying eg. (id=1)
    """
    detail_set = object.objects.filter(**kwargs)
    if detail_set:
        return detail_set
    else:
        raise Http404('No matches the given query.')


def check_ownership(
    request, user_id: int, force_ownership=False, force_authentication=False
) -> bool:
    """
    Checks if an user has the ownership over an account.
    Returns True if the user is the owner,
    The option force_ownership raises an 403 respone
    The Userid is for the Id the user needs to be to access this side
    """
    user = is_user_authenticated(request, force_authentication)
    if user:
        if user.id == user_id:
            return True
        elif force_ownership:
            raise PermissionDenied(
                'You\'re missing the access permissions to view this side'
            )
        else:
            return False
    else:
        return False
