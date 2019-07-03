
from django.contrib import admin
from django.urls import path, include
from chat import views
from django.conf import settings
from django.contrib.auth.views import LoginView
from django.conf.urls.static import static

urlpatterns = [
    path('chat/', include('chat.urls', namespace='chat')),
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    
    path('login/', LoginView.as_view(template_name='login.html'), name="login"),

    path('special/', views.special, name='special'),
    #path('^chat/', include('chat.urls')),
    path('logout/', views.user_logout, name='logout'),
    # path(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
    #     'document_root': settings.MEDIA_DIR}),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
