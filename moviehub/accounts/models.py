from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """rozšiřeni uzivatelskeho profilu o bio a avatar."""


    def avatar_path(self, filename):
        """cesta k avatar img"""
        return f"avatars/user_{self.user.id}/{filename}"


    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar= models.ImageField(blank=True, upload_to=avatar_path, null=True) #???
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

