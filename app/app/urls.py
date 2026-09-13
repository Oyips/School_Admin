from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from school_app import views as school_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', school_views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='school_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)