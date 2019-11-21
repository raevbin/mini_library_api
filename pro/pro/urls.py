from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from pro.settings import VERSION_API


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-v'+str(VERSION_API)+'/', include('library.urls')),
]
