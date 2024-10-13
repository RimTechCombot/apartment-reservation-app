from django.shortcuts import render, redirect
from .forms import AddVenueForm, EditVenueForm, AddImageForm, EditImageForm, AddReviewForm, EditReviewForm
from .models import Venue, VenueImage, Review
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
        elif request.POST.get("Review"):
            return redirect(f"/venue/{id}/review")
        elif request.POST.get("Edit Review"):
            return redirect(f"/venue/{id}/review/{request.POST['Edit Review']}/edit")
        elif request.POST.get("Delete Review"):
            Review.objects.get(id=request.POST['Delete Review']).delete()
    review_flag = True
    if Review.objects.filter(venue=id, owner=request.user.id):
        review_flag = False
    reviews = Review.objects.filter(venue=id)
    venue = Venue.objects.get(id=id)
    venue_images = VenueImage.objects.filter(venue=id)
    return render(request, "venue.html", {"venue": venue, "venue_images": venue_images, "reviews": reviews, "review_flag": review_flag})


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


def review(request, id):
    if request.method == "POST":
        form = AddReviewForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.venue = Venue.objects.get(id=id)
            obj.review = form.cleaned_data["review"]
            obj.rating = form.cleaned_data["rating"]
            obj.save()
            return redirect(f"/venue/{id}")
        else:
            return render(request, "add_review.html", {"form": form})
    form = AddReviewForm()
    return render(request, "add_review.html", {"form": form})


def edit_review(request, id, r_id):
    review = Review.objects.get(id=r_id)
    if request.method == "POST":
        form = EditReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect(f"/venue/{id}")
        else:
            return render(request, "edit_review.html", {"form": form})
    form = EditReviewForm(initial=model_to_dict(review))
    return render(request, "edit_review.html", {"review": review, "form": form})
