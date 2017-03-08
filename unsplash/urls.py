from django.conf.urls import url

from unsplash import curated
from unsplash import index_view
from unsplash import register
from . import views

urlpatterns = [
    url(r'^feed/', views.get_feed, name='getFeed'), #sends the random feed of unsplash
    url(r'^view', views.index, name='index'), #default view to add the photo (random feed photo)
    url(r'^register_phone', register.register_phone, name="register_phone"), #register phone devices
    url(r'^collection', curated.get_curated_list, name="curated"), #gets the collection list from unsplash
    url(r'^add_collection', curated.add_collections_photo, name="curated"), #adds the collection photo from unsplash
    url(r'^get_collection', curated.get_collection, name="curated"), #sends the collection names with details to app
    url(r'^get_photo_collection', curated.get_collections_photo, name='curated'), #sends a collections photo to app
    url(r'^$', index_view.original_index, name='original_index'), #original index, does nothing
]