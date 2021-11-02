from django.core.exceptions import BadRequest
from user_management.models import User
from tutor_smith.settings import EMAIL_USE_TLS
from django.contrib import messages
from django.views import View
from tutor_smith.utils import (
    check_ownership,
    display_messages,
    get_set_or_404,
    is_user_authenticated,
)
from django.shortcuts import get_object_or_404, redirect, render


class EditDetail(View):
    __context = {}
    detail = None
    FormClass = None
    template = 'detail_pages/edit.html'

    def get(self, request, id):
        self.__context['detail'] = get_object_or_404(self.detail, id=id)
        self.__context['isOwner'] = check_ownership(
            request, self.__context['detail'].author.id, True
        )
        self.__context['form'] = self.FormClass(
            detail=self.__context['detail']
        )

        return render(request, self.template, self.__context)

    def post(self, request, id, *args, **kwargs):
        self.__context['detailQ'] = get_set_or_404(self.detail, id=id)
        self.__context['detail'] = self.__context['detailQ'].first()
        self.__context['isOwner'] = check_ownership(
            request, self.__context['detail'].author.id, True
        )
        self.__context['form'] = self.FormClass(
            request.POST, detail=self.__context['detail']
        )

        if self.__context['form'].is_valid():
            self.__context['detailQ'].update(
                **self.__context['form'].cleaned_data
            )
            display_messages(request, 'Saved', messages.SUCCESS)
        else:
            display_messages(
                request, self.__context['form'].errors, messages.ERROR
            )
        return render(request, self.template, self.__context)


class AddDetail(View):
    context = {}
    detail = None
    FormClass = None
    template = 'detail_pages/edit.html'

    def get(self, request, *args, **kwargs):
        self.context['Owner'] = is_user_authenticated(request, True)
        self.context['form'] = self.FormClass(detail=None)

        return render(request, self.template, self.context)

    def post(self, request, *args, **kwargs):
        self.context['Owner'] = is_user_authenticated(request, True)
        self.check_perm(request, args=kwargs)
        self.context['form'] = self.FormClass(request.POST, detail=None)
        if self.context['form'].is_valid():
            try:
                info = self.create_model(args=kwargs)
                return redirect(
                    '/detail/' + info.get_type() + '/' + info.get_hashid()
                )
            except User.DoesNotExist:
                raise BadRequest('User does not exist')
            display_messages(request, 'Saved', messages.SUCCESS)
        else:
            display_messages(
                request, self.context['form'].errors, messages.ERROR
            )
        return render(request, self.template, self.context)

    def create_model(self, *args, **kwargs):
        return self.detail.objects.create(**self.context['form'].cleaned_data)

    def check_perm(self, request):
        return check_ownership(request, user_id=None)
