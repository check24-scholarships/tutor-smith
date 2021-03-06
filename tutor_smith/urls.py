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
from django.conf.urls.static import static
from . import settings

from user_management.models import Info, Review
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path, register_converter
from user_management import views as user_views

from .converters import (
    ResetHashIdConverter,
    UserHashIdConverter,
    MultipleHashIdConverter,
)

# Registers Converters
register_converter(UserHashIdConverter, 'user_hashid')
register_converter(MultipleHashIdConverter, 'multiple_hashid')
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

detailpatterns = [
    path(
        'info/<user_hashid:id>/',
        user_views.detail_view,
        {'detail_class': Info, 'template': 'detail_pages/detail_info.html'},
    ),
    path(
        'review/<user_hashid:id>/',
        user_views.detail_view,
        {
            'detail_class': Review,
            'template': 'detail_pages/detail_review.html',
        },
    ),
    # Edit paths
    path(
        'info/<user_hashid:id>/edit/',
        user_views.EditInfo.as_view(),
        name='edit_review',
    ),
    path(
        'review/<user_hashid:id>/edit/',
        user_views.EditReview.as_view(),
        name='edit_review',
    ),
    # Adder paths
    path('info/add/', user_views.AddInfo.as_view(), name='add_info'),
    path(
        'review/<user_hashid:user_id>/add',
        user_views.AddReview.as_view(),
        name='add_review',
    ),
    # Deletion paths
    path(
        'info/<user_hashid:id>/delete/',
        user_views.delete_detail,
        {'detail': Info, 'redirect_url': '/'},
    ),
    path(
        'review/<user_hashid:id>/delete/',
        user_views.delete_detail,
        {'detail': Review, 'redirect_url': '/'},
    ),
]

requestpatterns = [
    path(
        'add/<user_hashid:info_id>/',
        user_views.request_contact,
        name='request',
    ),
    path('list/', user_views.show_requests, name='list_request'),
    path(
        'accept/',
        user_views.accept_request,
        name='accept_request',
    ),
    path(
        'delete/',
        user_views.delete_request,
        name='delete_request',
    ),
]

staffpatterns = [
    path('', user_views.staff_index, name='staff_index'),
    path('list/', user_views.list_tickets, name='staff_list'),
    path('add_ticket/', user_views.add_ticket),
    path('add_report/<user_hashid:user_id>/', user_views.add_report),
    # path('delete_ticket/<user_hashid:id>', user_views.delete_),
    path(
        'accept_ticket/<multiple_hashid:ticket_id>/',
        user_views.accept_ticket,
        name='accept_ticket',
    ),
    path(
        'delete_ticket/',
        user_views.delete_ticket,
        name='delete_ticket',
    ),
    path('ticket_send/', user_views.ticket_send, name='ticket_send'),
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
    path(
        'users/edit/<user_hashid:user_id>/',
        user_views.user_edit,
        name='profile_edit',
    ),
    # Reset patterns will have the path: reset/..../...
    path('reset/', include(resetpatterns)),
    path('detail/', include(detailpatterns)),
    path('request/', include(requestpatterns)),
    path('staff/', include(staffpatterns)),
    path('search', user_views.search, name='search'),
    # path('search', user_views.view_all, name='view_all'),
    path('all', user_views.view_all, name='view_all'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
