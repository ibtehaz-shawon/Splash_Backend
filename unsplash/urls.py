from django.conf.urls import url

from unsplash import index_view
from . import views

urlpatterns = [
    url(r'^feed/', views.get_feed, name='getFeed'),
    url(r'^view', views.index, name='index'),
    url(r'^$', index_view.original_index, name='original_index'),
]