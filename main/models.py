from django.db import models
from django.contrib.auth.views import get_user_model
from django.template.defaultfilters import slugify
from os.path import splitext
from mptt.models import MPTTModel, TreeForeignKey

User = get_user_model()


# Create your models here.

def slugify_upload(instance, filename):
    folder = instance._meta.model_name
    name, ext = splitext(filename)
    name_t = slugify(name) or name
    return f"{folder}/{name_t}{ext}"


class Category(MPTTModel):
    name = models.CharField(max_length=250)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, null=True)
    expires_at = models.DateTimeField(auto_now_add=True)
    product_type = models.JSONField(null=True)
    image = models.ImageField(upload_to=slugify_upload, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            if self.category.parent:
                self.slug = slugify(f'{self.category.parent.name, self.category.name}')
            else:
                self.slug = slugify(f'{self.category.name}')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.category.name


class Favourite(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
