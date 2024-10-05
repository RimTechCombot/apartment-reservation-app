from django.shortcuts import render, redirect
from .forms import AddVenueForm, EditVenueForm, AddImageForm, EditImageForm
from .models import Venue, VenueImage
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
        if request.POST.get("Delete Venue"):
            Venue.objects.filter(id=request.POST["Delete Venue"]).delete()
            return redirect("/list-venue")
    venues = Venue.objects.all()
    return render(request, "list_venue.html", {"venues": venues})


def edit_venue(request, id):
    venue = Venue.objects.get(id=id)
    if request.method == "POST":
        form = EditVenueForm(request.POST, request.FILES, instance=venue)
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
        if request.POST.get("Delete Venue"):
            Venue.objects.filter(id=request.POST["Delete Venue"]).delete()
            return redirect("/list-venue")
    venues = Venue.objects.filter(owner=request.user)
    return render(request, "my_venues.html", {"venues": venues})


def venue(request, id):
    if request.method == "POST":
        if request.POST.get("Edit Venue"):
            return redirect(f"/edit-venue/{request.POST['Edit Venue']}")
        elif request.POST.get("Add Images"):
            return redirect(f"/venue/{request.POST['Add Images']}/add-images")
    venue = Venue.objects.get(id=id)
    venue_images = VenueImage.objects.filter(venue=id)
    return render(request, "venue.html", {"venue": venue, "venue_images": venue_images})


def add_images(request, id):
    venue = Venue.objects.get(id=id)
    if request.method == "POST":
        form = AddImageForm(request.POST, request.FILES)
        if form.is_valid():
            for image in request.FILES.getlist('image'):
                image_obj = VenueImage(venue=venue, image=image)
                image_obj.save()
            return redirect(f"/venue/{id}")
        else:
            return render(request, "add_images.html", {"form": form, "venue": venue})
    form = AddImageForm()
    return render(request, "add_images.html", {"form": form, "venue": venue})


def venue_image(request, id, vi_id):
    venue_image = VenueImage.objects.get(id=vi_id)
    if request.method == "POST":
        if request.POST.get("Edit VenueImage"):
            return redirect(f"/venue/{id}/edit-image/{vi_id}")
        elif request.POST.get("Delete Image"):
            venue_image.delete()
            return redirect(f"/venue/{id}")
    return render(request, "venue_image.html", {"venue_image": venue_image})


def edit_venue_image(request, id, vi_id):
    venue_image = VenueImage.objects.get(id=vi_id)
    if request.method == "POST":
        form = EditImageForm(request.POST, request.FILES, instance=venue_image)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.image = form.cleaned_data["image"]
            obj.save()
            return redirect(f"/venue/{id}")
        else:
            return render(request, "edit_venue_image.html", {"form": form})
    form = EditImageForm(initial=model_to_dict(venue_image))
    return render(request, "edit_venue_image.html", {"venue_image": venue_image, "form": form})
