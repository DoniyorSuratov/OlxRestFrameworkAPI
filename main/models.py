from django.db import models
from django.contrib.auth.views import get_user_model
from django.template.defaultfilters import slugify
from os.path import splitext
User = get_user_model()
# Create your models here.

def slugify_upload(instance, filename):
    folder = instance._meta.model_name
    name, ext = splitext(filename)
    name_t = slugify(name) or name
    return f"{folder}/{name_t}{ext}"

class CreateAdvertisementDetskiymir(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    slug = models.SlugField(blank=True, null=True)
    price =models.FloatField(blank=True, null=True)
    color = models.CharField(max_length=30, blank=True, null=True)
    expires_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title