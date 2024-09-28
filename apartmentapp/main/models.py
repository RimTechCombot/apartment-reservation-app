from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class Venue(models.Model):

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.TextField(max_length=50)
    image = models.ImageField(upload_to='media')
    description = models.TextField(max_length=200)

