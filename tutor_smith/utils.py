from typing import List
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models.query import QuerySet
from django.http.response import Http404, HttpResponse
from .converters import h_decode, user_hasher
from user_management.models import User

from django.core.mail import send_mail
from tutor_smith.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string

import os.path as path

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
    request,
    user_id: int,
    force_ownership=False,
    force_authentication=False,
    return_user=False,
):
    """
    Checks if an user has the ownership over an account.
    Returns True if the user is the owner,
    The option force_ownership raises an 403 respone
    The Userid is for the Id the user needs to be to access this side
    """
    user = is_user_authenticated(request, force_authentication)
    if user:
        if user.id == user_id:
            if return_user:
                return (True, user)
            else:
                return True
        elif force_ownership:
            raise PermissionDenied(
                'You\'re missing the access permissions to view this side'
            )

    if return_user:
        return (False, user)
    return False


def is_user_staff(request, force_staff=False, force_authentication=False):
    user = is_user_authenticated(request, force_authentication)
    if user:
        try:
            User.objects.get(id=user.id, is_staff=True)
            return True
        except:
            pass
    if force_staff:
        raise PermissionDenied('Not enough rights')
    return False


def send_custom_email(recepients: list, template, content: dict, subject):
    """
    Sends an email to the user
    Takes in:
    - a list of recepients,
    - a template name (example: password_reset_email.html) --> must be placed in the templates/emails folder,
    - a content dict containing the variables for the template,
    - a subject
    """
    email_template_path = path.join('emails', template)
    email = render_to_string(email_template_path, content)

    send_mail(
        subject,
        email,
        EMAIL_HOST_USER,
        recepients,
        fail_silently=False,
    )


def prepare_multiple_hashids(request):
    """
    takes multiple request GET arguments ?hashid1=on&hashid2=on
    and returns a list of ids
    """
    try:
        g = dict(request.GET).keys()
    except:
        return HttpResponse(406)
    prep = []
    for _ in g:
        prep.append(h_decode(user_hasher, _))
    return prep
