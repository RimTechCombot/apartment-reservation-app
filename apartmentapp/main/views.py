from django.shortcuts import render
from .forms import AddVenueForm
from .models import Venue


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
    venues = Venue.objects.all()
    return render(request, "list_venue.html", {"venues": venues})


def edit_venue(request, id):
    venue = Venue.objects.get(id=id)
    return render(request, "edit_venue.html", {"venue":venue})