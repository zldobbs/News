from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='newsfeed-index'),
    path('source/<int:source_id>/', views.source, name='source'),
    path('author/<int:author_id>/', views.author, name='author')
]