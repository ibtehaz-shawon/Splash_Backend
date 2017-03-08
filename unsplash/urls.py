from django.conf.urls import url

from unsplash import curated
from unsplash import index_view
from unsplash import register
from . import views

urlpatterns = [
    url(r'^feed/', views.get_feed, name='getFeed'),
    url(r'^view', views.index, name='index'),
    url(r'^register_phone', register.register_phone, name="register_phone"),
    url(r'^collection', curated.get_curated_list, name="curated"),
    url(r'^add_collection', curated.add_collections_photo, name="curated"),
    url(r'^get_collection', curated.get_collection, name="curated"),
    url(r'^$', index_view.original_index, name='original_index'),
]