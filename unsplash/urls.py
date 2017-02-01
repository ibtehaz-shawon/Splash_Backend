from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^feed/', views.get_feed, name='getFeed'),
    url(r'^$', views.index, name='index'),
]