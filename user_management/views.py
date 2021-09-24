# HTML Handeling
from user_management.custom_class_views import AddDetail
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseServerError
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.db.models import Q

from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from tutor_smith.utils import *

from django.core.mail import send_mail
from tutor_smith.settings import EMAIL_HOST_USER

from .custom_class_views import *
from .forms import *
from .models import User, Info, Review, Settings
from .validators import validate_login, validate_register, validate_recover
from .choices import *
from tutor_smith.converters import reset_hasher, h_encode, h_decode


dict_gender = dict(choice_gender)


def index(request):
    __context = {'users': User.objects.all()}
    return render(request, 'index.html', __context)


def recover_form(request):
    if request.method == 'POST':
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            # Send email...
            """associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:"""
            # get users
            # ADD LAST LOGIN attribute to user for password recover to fully work
            # user = User.objects.get(email=data)
            # default_token_generator.make_token(user)
            try:
                # Get user by email entered in form
                user = User.objects.get(email=data)
                print(user.password)
                email_template_name = 'password/password_reset_email.txt'
                content = {
                    'subject': 'Password Recover Requested',
                    'email': 'shizhe.he6@gmail.com',
                    'domain': '127.0.0.1:8000',
                    'site_name': 'Website',
                    'uid': h_encode(
                        reset_hasher, user.id
                    ),  # generate user hashid for password reset
                    'user': 'test',
                    'token': 0,  # default_token_generator.make_token(user),
                    'protocol': 'http',
                }
                email = render_to_string(email_template_name, content)
                recepient = 'shizhe.he6@gmail.com'

                send_mail(
                    content['subject'],
                    email,
                    EMAIL_HOST_USER,
                    [recepient],
                    fail_silently=False,
                )
                messages.success(
                    request,
                    'A message with reset password instructions has been sent to your inbox.',
                )

                return redirect('/reset/sent/')

            except Exception:
                messages.add_message(
                    request,
                    messages.INFO,
                    'An invalid email has been entered.',
                )

    password_reset_form = PasswordResetForm()
    return render(
        request,
        'password/password_reset.html',
        context={'password_reset_form': password_reset_form},
    )


def recover_form_sent(request):
    return render(request, 'password/password_reset_sent.html')


def recover_form_confirm(request, uidb64, token):
    # get session validity

    if request.method == 'POST':
        form = ResetForm(request.POST)
        res = validate_recover(request, form)
        uid = h_decode(reset_hasher, uidb64)  # get user id
        user = User.objects.get(id=uid)

        if res:
            user.password = form.cleaned_data[
                'password_1'
            ]  # not great, but works for now
            # user.set_password(form.cleaned_data['password_1'])
            user.save()

            return redirect('/reset/done/')

    form = ResetForm()
    return render(
        request,
        'password/password_reset_confirm.html',
        context={'form': form},
    )


def recover_form_complete(request):
    return render(request, 'password/password_reset_complete.html')


def search(request):
    if request.method == 'POST':
        search = request.POST['searched']
        if search:
            # get users associated with search value
            users = User.objects.filter(
                Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(email__icontains=search)
            )
            return render(
                request, 'search.html', {'search': search, 'users': users}
            )

    return render(request, 'search.html', {})


def register(request):
    __context = {'form': None}
    if request.method == 'POST':
        form = UserForm(request.POST)

        res = validate_register(request, form)
        if res:
            user = User(
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                gender=form.cleaned_data['gender'],
                address=form.cleaned_data['address'],
                phone=form.cleaned_data['phone'],
                user_class=form.cleaned_data['user_class'],
                birth_date=form.cleaned_data['birth_date'],
                ip=get_client_ip(request),
            )
            user.set_password(form.cleaned_data['password_1'])
            user.create_default_data()
            user.save()
            user_settings = Settings(user=user)
            user_settings.create_default()
            user_settings.save()
            request.session['user'] = user.id
            messages.add_message(request, messages.SUCCESS, 'Nutzer erstellt!')
            return redirect('/login')
    # Displays Form and Context on view when not returned before
    form = UserForm()
    __context['form'] = form
    return render(request, 'register.html', context=__context)


def login(request):
    # redirect if the user is authenticated
    try:
        if request.session['userid']:
            return redirect('/')
    except KeyError:
        pass

    __context = {'form': None}
    if request.method == 'POST':
        # Test cookie looks if cookies are enabled.
        if not request.session.test_cookie_worked():
            return HttpResponse('Please Enable Cookies')
        request.session.delete_test_cookie()
        form = LoginForm(request.POST)
        user = validate_login(request, form)
        if user:
            request.session['userid'] = user.get_hashid()
            user.ip = get_client_ip(request)
            user.save()
            return redirect('/')

    form = LoginForm()
    __context['form'] = form
    request.session.set_test_cookie()
    return render(request, 'login.html', __context)


def logout(request):
    request.session.flush()
    # TODO: Find better solution (Template, Variable)
    return HttpResponse(
        '<script>setTimeout(function(){window.location.href = \'/\';}, 2000);</script><p>Logged out! if you don\'t get redirected after 2 secounds click <a href=\"/\">here</a></p>'
    )


@csrf_exempt
def user_profile(request, user_id, subpath):
    # Uses HTMX for Reactive Design
    __context = {
        'user': get_object_or_404(User, id=user_id),
    }
    __context['isOwner'] = check_ownership(request, __context['user'].id)

    __context['settingsQ'] = Settings.objects.filter(user=__context['user'])
    if not __context['settingsQ']:
        return HttpResponseServerError()
    __context['settings'] = __context['settingsQ'].first()
    # ----------------
    if subpath == 'profile':
        __context['gender'] = dict_gender[__context['user'].gender]
        __context['review'] = (
            Review.objects.filter(for_user=__context['user'])
            .order_by('-stars')
            .first()
        )
        return render(request, 'profile/profile.html', __context)
    # ----------------
    elif subpath == 'infos':
        __context['infos'] = Info.objects.filter(author=__context['user'])
        return render(request, 'profile/infos.html', __context)
    # -----------------
    elif subpath == 'reviews':
        __context['reviews'] = Review.objects.filter(
            for_user=__context['user']
        )
        __context['isAuth'] = is_user_authenticated(request)
        return render(request, 'profile/reviews.html', __context)
    # -----------------
    elif subpath == 'edit':
        __context['isOwner'] = check_ownership(
            request, __context['user'].id, True
        )
        if request.method == 'POST':
            form = ProfileEditForm(
                request.POST,
                user=__context['user'],
                settings=__context['settings'],
            )
            if form.is_valid():
                # TODO: Change for more  method
                __context['user'].description = form.cleaned_data[
                    'description'
                ]
                __context['user'].save()
                __context['settingsQ'].update(form.cleaned_data)

                messages.add_message(request, messages.SUCCESS, 'saved')

        __context['form'] = ProfileEditForm(
            user=__context['user'], settings=__context['settings']
        )
        return render(request, 'profile/edit.html', __context)
    else:
        return Http404()


def detail_view(request, id, *args, **kwargs):
    # print(kwargs['detail_class'].objects.filter(id=id).first().get_hashid())
    __context = {'isOwner': is_user_authenticated(request)}
    __context['detail'] = get_object_or_404(kwargs['detail_class'], id=id)
    if __context['isOwner']:
        __context['isOwner'] = (
            __context['detail'].author == __context['isOwner']
        )
    return render(request, kwargs['template'], __context)


class EditInfo(EditDetail):
    detail = Info
    FormClass = InfoEditForm


class EditReview(EditDetail):
    detail = Review
    FormClass = ReviewEditForm


class AddInfo(AddDetail):
    detail = Info
    FormClass = InfoEditForm

    def create_model(self, *args, **kwargs):
        self.detail.objects.create(
            **self.context['form'].cleaned_data,
            author=self.context['Owner'],
            created_on=timezone.now()
        )

    def check_perm(self, request, *args, **kwargs):
        return True


class AddReview(AddDetail):
    detail = Review
    FormClass = ReviewEditForm

    def create_model(self, *args, **kwargs):
        self.detail.objects.create(
            author=self.context['Owner'],
            for_user=User.objects.get(id=kwargs['args']['user_id']),
            created_on=timezone.now(),
            **self.context['form'].cleaned_data
        )

    def check_perm(self, request, *args, **kwargs):
        if check_ownership(request, kwargs['args']['user_id']):
            raise PermissionDenied(
                'you are the owner of the review your trying to write'
            )


def delete_detail(request, id, *args, **kwargs):
    obj = get_object_or_404(kwargs['detail'], id=id)
    check_ownership(request, obj.author.id, True, True)
    obj.delete()
    display_messages(request, 'Deleted', messages.SUCCESS)
    return redirect(kwargs['redirect_url'])
