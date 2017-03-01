from django.conf.urls import url

from unsplash import curated
from unsplash import index_view
from unsplash import register
from . import views

urlpatterns = [
    url(r'^feed/', views.get_feed, name='getFeed'),
    url(r'^view', views.index, name='index'),
    url(r'^register_phone', register.register_phone, name="register_phone"),
    url(r'^get_curated', curated.get_curated_list, name="curated"),
    url(r'^$', index_view.original_index, name='original_index'),
]