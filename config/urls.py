"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.views.generic import TemplateView
from config import settings ##No good
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('workingtime.urls', namespace='workingtime')),
]
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     #path('', hello, name='home'),#WRONG
#     # path('', TemplateView.as_view(template_name='users/home.html'), name='home'),
#     path('', include('catalog.urls', namespace='catalog')),
#     path('users/', include('users.urls', namespace='users')),
#     path('users/password_reset', TemplateView.as_view(template_name='registration/password_reset_form.html'),
#          name='password_reset'),
# ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
