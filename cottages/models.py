from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
from django.utils import timezone
import itertools


STATUS = ((0, "Draft"), (1, "Published"))


# Create your models here.
class Cottage(models.Model):

    cottage_id = models.CharField(
        primary_key=True,
        max_length=20,
        default="Pen Y Graig"
    )
    featured_image = CloudinaryField('image', default='placeholder')
    description = models.CharField(
        max_length=400,
        blank=True,
        null=True,
        default="Untitled Cottage"
    )
    slug = models.SlugField(max_length=200, blank=True)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    max_guests = models.IntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    
    @property
    def pretty_name(self):
        return self.slug.replace('-', ' ').title()
    def image_url(self):
        if self.cloudinary_url:
            return self.cloudinary_url
        elif self.image:
            return self.image.url
        return ''

    def __str__(self):
        return f"{self.cottage_id} Cottage"


def unique_slugify(instance, slug_field, slug_source):
    slug = slugify(slug_source)
    ModelClass = instance.__class__
    unique_slug = slug
    for i in itertools.count(1):
        if not ModelClass.objects.filter(**{slug_field: unique_slug}).exists():
            break
        unique_slug = f"{slug}-{i}"
    setattr(instance, slug_field, unique_slug)


class CottageImage(models.Model):
    cottage = models.ForeignKey(Cottage, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='cottages/')
    caption = models.CharField(max_length=255, blank=True)
    import_batch_id = models.CharField(max_length=100, blank=True, null=True)


class HeroImage(models.Model):
    image = models.ImageField(upload_to='hero/')
    caption = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.caption or self.image.name


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    guest = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviewer")
    cottage = models.ForeignKey(
        Cottage, on_delete=models.CASCADE, related_name="reviews")
    title = models.CharField(max_length=120)
    featured_image = CloudinaryField('image', default='placeholder')
    rating = models.IntegerField(
        default=0,
        choices=[(i, str(i)) for i in range(1, 6)],
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    body = models.TextField(max_length=200)
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slugify(self, 'slug', self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Review by {self.guest} on {self.cottage}"
    class Meta:
        unique_together = ('guest', 'cottage', "created_on")
        ordering = ["created_on"]
