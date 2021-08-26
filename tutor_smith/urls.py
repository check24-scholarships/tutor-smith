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
from django.urls import path, include, register_converter

from user_management import views as user_views
from .converters import HashIdConverter

register_converter(HashIdConverter, 'hashid')

urlpatterns = [
    # TODO: Remove admin when finished
    path('admin/', admin.site.urls),
    path('', user_views.index),
    path('register/', user_views.register),
    path('login/', user_views.login),
    path('users/<hashid:user_id>/', user_views.user_profile)
]
