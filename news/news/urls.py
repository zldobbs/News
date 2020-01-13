from django.contrib import admin
from django.conf.urls import handler404, handler500
from django.urls import include, path

from . import views

handler404 = views.handle404
# handler500 = views.handle500

urlpatterns = [
    path('', views.index, name="news-index"),
    path('newsfeed/', include('newsfeed.urls')),
    path('admin/', admin.site.urls)
]