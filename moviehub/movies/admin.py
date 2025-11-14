from django.contrib import admin
from django.contrib.auth.models import User

from .models import Movie,Actor,Genre

# Register your models here.
# admin.site.register(Movie)
admin.site.register(Actor)

# admin.site.register(Genre)
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug":("name",)}


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "release_date", "slug")
    prepopulated_fields = {"slug":("title",)}
    list_filter = ("genres", "release_date")