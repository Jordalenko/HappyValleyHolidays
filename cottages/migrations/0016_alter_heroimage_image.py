# Generated by Django 4.2.21 on 2025-06-12 14:28

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cottages', '0015_heroimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='heroimage',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
    ]
