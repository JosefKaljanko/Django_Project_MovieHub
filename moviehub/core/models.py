from django.db import models
# from django.contrib.auth.models import (User,
#                                         UserManager,Group,GroupManager,Permission,PermissionManager,PermissionsMixin,
#                                         AnonymousUser,AbstractUser)

from django.contrib.auth.models import User

class Genre(models.Model):
    """
    Model žánru filmu(akce, drama, komedie,...)
    """
    name = models.CharField(max_length=70)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name