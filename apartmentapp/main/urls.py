from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-venue', views.add_venue, name='add-venue'),
    path('list-venue', views.list_venue, name='list-venue'),
    path('edit-venue/<int:id>', views.edit_venue, name='edit-venue'),
    path('my-venues', views.my_venues, name='my-venues'),
    path('venue/<int:id>', views.venue, name='venue'),
    path('venue/<int:id>/add-images', views.add_images, name='add-images'),
    path('venue/<int:id>/venue-image/<int:vi_id>', views.venue_image, name='venue-image'),
    path('venue/<int:id>/edit-image/<int:vi_id>', views.edit_venue_image, name='edit-image'),
]
