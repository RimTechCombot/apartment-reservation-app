from django import forms
from django.forms import ModelForm, Form, FileField
from django.contrib.auth.models import User
from .models import Venue, VenueImage


class AddVenueForm(ModelForm):

    class Meta:
        model = Venue
        fields = ["name", "description", "image", "is_active", "price"]


class EditVenueForm(ModelForm):

    class Meta:
        model = Venue
        fields = ["name", "description", "image", "is_active", "price"]


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class AddImageForm(ModelForm):

    image = MultipleFileField()

    class Meta:
        model = VenueImage
        fields = ["image"]


class EditImageForm(ModelForm):

    class Meta:
        model = VenueImage
        fields = ["image"]
