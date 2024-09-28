from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Venue


class AddVenueForm(ModelForm):

    class Meta:
        model = Venue
        fields = ["name", "description", "image"]