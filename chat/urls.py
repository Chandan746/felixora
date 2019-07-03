from django.urls import path, include, re_path
from . import views
app_name = 'chat'

urlpatterns = [
    #path('', views.index, name='index'),
    #path('chat/', views.c_index, name='chat'),
    re_path('^(?P<room_name>[^/]+)/(?P<usr_id>[^/]+)/$',
            views.room, name='room'),
    re_path(r'^register/$', views.register, name='register'),
    re_path(r'^user_login/$', views.user_login, name='user_login'),
]
