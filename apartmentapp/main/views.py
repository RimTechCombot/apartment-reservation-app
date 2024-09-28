from django.shortcuts import render, redirect
from .forms import AddVenueForm, EditVenueForm
from .models import Venue
from django.forms.models import model_to_dict


def home(request):
    return render(request, "home.html")


def add_venue(request):
    if request.method == "POST":
        form = AddVenueForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.image = form.cleaned_data["image"]

            obj.save()
            return render(request, "home.html")
        else:
            return render(request, "add_venue.html", {"form": form})
    form = AddVenueForm()
    return render(request, "add_venue.html", {"form": form})


def list_venue(request):
    if request.method == "POST":
        if request.POST.get("Edit Venue"):
            return redirect(f"/edit-venue/{request.POST['Edit Venue']}")

    venues = Venue.objects.all()
    return render(request, "list_venue.html", {"venues": venues})


def edit_venue(request, id):
    venue = Venue.objects.get(id=id)
    if request.method == "POST":
        form = EditVenueForm(request.POST, request.FILES, instance=venue)
        print(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.image = form.cleaned_data["image"]
            obj.save()
            return render(request, "home.html")
        else:
            return render(request, "edit_venue.html", {"form": form})
    form = EditVenueForm(initial=model_to_dict(venue))
    return render(request, "edit_venue.html", {"venue": venue, "form": form})


def my_venues(request):
    if request.method == "POST":
        if request.POST.get("Edit Venue"):
            return redirect(f"/edit-venue/{request.POST['Edit Venue']}")
    venues = Venue.objects.filter(owner=request.user)
    return render(request, "my_venues.html", {"venues": venues})
