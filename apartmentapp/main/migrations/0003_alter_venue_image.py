# Generated by Django 4.2.16 on 2024-09-27 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_alter_venue_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="venue",
            name="image",
            field=models.ImageField(upload_to="media"),
        ),
    ]
