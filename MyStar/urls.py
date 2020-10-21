"""MyStar URL Configuration

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
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_jwt import views as jwt_views
import admin_tools.urls
from users.kassa import YandexNotification, YandexPayment

urlpatterns = [
    path('admin/', admin.site.urls),

    # users end point
    path('api/', include('users.urls')),
    path('auth/', include('rest_framework_social_oauth2.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^password_reset/', include('django_rest_passwordreset.urls')),

    re_path(r'^payments/', YandexPayment.as_view()),
    re_path(r'^payments/notifications/', YandexNotification.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
