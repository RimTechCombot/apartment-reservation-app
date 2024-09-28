from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-venue', views.add_venue, name='add-venue'),
    path('list-venue', views.list_venue, name='list-venue'),
    path('edit-venue/<int:id>', views.edit_venue, name='edit-venue'),
    path('my-venues', views.my_venues, name='my-venues'),
]
