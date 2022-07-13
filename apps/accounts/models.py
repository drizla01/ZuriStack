from random import random
from tabnanny import verbose
from django.db import models
from django.forms import SelectDateWidget
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from . import utils

# Create your models here.
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    # phone = models.CharField()
    slug = models.SlugField(blank=True, unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        verbose_name = "User"
        ordering = ["email"]

    def __str__(self):
        return self.email

    # create a default slug/username for users if blank

    def gen_random_slug(self):
        random_slug = slugify(
            self.first_name + self.last_name + utils.generate_random_id()
        )
        while CustomUser.objects.filter(slug=random_slug).exists():
            random_slug = slugify(
                self.first_name + self.last_name + utils.generate_random_id()
            )
        return random_slug

    def save(self, *args, **kwargs):
        # perform some logic
        # that checks for a slug

        if not self.slug:
            # create default slug
            self.slug = self.gen_random_slug()
        # finally save
        super().save(*args, **kwargs)
