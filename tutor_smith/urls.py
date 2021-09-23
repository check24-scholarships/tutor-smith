"""tutor_smith URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path, register_converter
from user_management import views as user_views

from .converters import ResetHashIdConverter, UserHashIdConverter

# Registers Converters
register_converter(UserHashIdConverter, 'user_hashid')
register_converter(ResetHashIdConverter, 'reset_hashid')

# All reset patterns
resetpatterns = [
    path('', user_views.recover_form, name='recover_password'),
    path('sent/', user_views.recover_form_sent),
    path(
        '<uidb64>/<token>/',
        user_views.recover_form_confirm,
        # auth_views.PasswordResetConfirmView.as_view(
        #    template_name='password/password_reset_confirm.html'
        # ),
        name='password_reset_confirm',
    ),
    path(
        'done/',
        user_views.recover_form_complete,
        name='password_reset_complete',
    ),
]


urlpatterns = [
    # TODO: Remove admin when finished
    path('admin/', admin.site.urls),
    path('', user_views.index, name='index'),
    path('register/', user_views.register, name='register'),
    path('login/', user_views.login, name='login'),
    path('logout/', user_views.logout, name='logout'),
    path(
        'users/<user_hashid:user_id>/<str:subpath>',
        user_views.user_profile,
        name='profile',
    ),
    # Reset patterns will have the path: reset/..../...
    path('reset/', include(resetpatterns)),
]
