"""vschools URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('resource.urls')),
    path('live/', include('live.urls')),
    path('schedules/', meeting_schedules, name="schedules"),
    path('guest/',guest_page, name = "guest"),
    path('login/', user_login, name='login'),
    path('login/',login_page, name = "log-in"),
    path('homepage', home_page, name = "home2"),
    path('get_started/', get_started_page, name = "get_started"),
    path('get_token/', getToken, name = "getToken"),
    path('email_verify/',verify_email_page, name = "verify_email_page"),
    path('update_username/',update_username),
    path('update_password/',update_password),
    path('whiteboard/<str:meeting_id>',whiteboard_page),
    path('logout/',logout_user, name = "logout"),
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('sign_up/',sign_up_page, name = "sign_up"),
    path('settings/',settings_page, name = "settings"),
    path('schedule_meeting/', schedule_meeting, name = "schedule"),
    path('new_password/', new_password_page, name = "new_password"),
    path('ask_delete/',ask_delete_page, name = "ask_delete"),
    path('join_session/', join_session, name = "join_session"),
    path('meeting_ended/',meeting_ended, name = "meeting_ended"),
    path('whiteboardDetails/', whiteboardDetails, name = "whiteboardDetails"),
    path('start_meeting/',start_meeting, name = "start_meeting"),
    path('changeWhiteboardDetails/', changeWhtieboardDetails, name = "changeWhtieboardDetails"),
    path('UpdateWhiteboardDetails/', UpdateWhiteboardDetails),
    path('recorded_meetings/', recorded_files, name = "recorded_files"),
    path('files/<str:meeting_id>',uploaded_files, name = "uploaded_files"),
    path('verify/<str:token>',verify_email),
    path('test/', test_page, name = "test"),
    path('meet/<str:meeting_id>',meet_page, name = "meet"),
    path('live_ended/',live_stream_ended, name="live_ended"),
    path('person/<str:user_token>',person_info_page, name = "person_info"),
    path('reset',auth_views.PasswordResetView.as_view(template_name="forgot_password.html"), 
        name = "reset_password"),
    path('reset_sent/',
            auth_views.PasswordResetDoneView.as_view(template_name="email_verification.html"), 
            name = "password_reset_done"),
    path('reset/<uidb64>/<token>',
            auth_views.PasswordResetConfirmView.as_view(template_name="change_password.html"), 
            name = "password_reset_confirm"),
    path('reset_complete',
            auth_views.PasswordResetCompleteView.as_view(template_name="password_changed.html"), 
            name = "password_reset_complete"),

    
    path('logout/', logout_view, name='user_logout'),
    path('profile/', profile, name='profile'),
    path('profile/update/', AccountInfoUpdateView.as_view(), name='profile_update'),
    path('create-superuser/', create_superuser, name='create_superuser'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



