from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # AbstractUser automatically provides: username, email, password, and date_joined!
    # We are keeping this empty for now with 'pass', but setting it up this way 
    # means we can easily add custom fields (like 'avatar' or 'bio') in Version 2.0.
    pass

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, help_text="The URL-friendly version of the name.")
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories" # Fixes a typo in the Django Admin so it doesn't say "Categorys"

    def __str__(self):
        return self.name