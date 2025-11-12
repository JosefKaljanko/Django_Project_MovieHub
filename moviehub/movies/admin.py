from django.contrib import admin
from django.contrib.auth.models import User

from .models import Movie,Actor,Genre

# Register your models here.
admin.site.register(Movie)
admin.site.register(Actor)
admin.site.register(Genre)
# admin.site.register(User)

