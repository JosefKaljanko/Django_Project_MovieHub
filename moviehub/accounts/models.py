from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """rozšiřeni uzivatelskeho profilu o bio a avatar."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar= models.ImageField(blank=True, upload_to="avatars/", null=True) #???
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username