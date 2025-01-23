
from django.db import models

class Admin(models.Model):
    is_active = models.BooleanField(default=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)


class Facility(models.Model):
    name = models.CharField(max_length=255)
    location = models.TextField()
    department = models.CharField(max_length=255)
    resources = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
