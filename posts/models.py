from django.db import models
import random
import os
import string
from django.utils.text import slugify


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    new_filename = random.randint(1, 151251251)
    name, ext = os.path.splitext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)

    return f"post_images/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)
# Create your models here.
class Post(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to=upload_image_path, blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.content[:50]) or "post"
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)