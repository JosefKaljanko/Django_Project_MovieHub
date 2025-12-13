from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.html import format_html

from .models import Movie,Actor,Genre

# Register your models here.
# admin.site.register(Movie)
admin.site.register(Actor)

# admin.site.register(Genre)
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug":("name",)}


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "release_date", "slug",
                    "poster_preview", "avg_rating_display",)
    list_display_links = ("poster_preview","title")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug":("title",)}
    list_filter = ("genres", "release_date")
    filter_horizontal = ("genres","actors")
    readonly_fields = ("poster_preview_large",)

    fieldsets = (
        ("Základ", {
            "fields": ("title", "slug", "release_date", "description")
        }),
        ("Plakát", {
            "fields": ("poster_image", "poster_url", "poster_preview_large")
        }),
        ("Vazby", {
           "fields": ("genres", "actors")
        }),
    )

    def poster_preview(self, obj):
        """Malý náhled do listu."""
        url = None
        if obj.poster_image:
            url = obj.poster_image.url
        elif obj.poster_url:
            url = obj.poster_url

        if not url:
            return "--"

        return format_html(
            f"<img src='{url}' style='height:48px'; width:32px; object-fit:cover; border-radius:4px; />",
            url=url
        )

    poster_preview.short_description = "Poster"

    def poster_preview_large(self, obj):
        """Veký náhled v detailu (read-only)"""
        url = None
        if obj.poster_image:
            url = obj.poster_image.url
        elif obj.poster_url:
            url = obj.poster_url

        if not url:
            return "No poster image"

        return format_html(
            f"<img src='{url}' style='max-height:260px; object-fit:cover; border-radius:10px;' />",
            url=url
        )
    poster_preview_large.short_description = "Náhled"

    def avg_rating_display(self, obj):
        return "--"

    avg_rating_display.short_description = "Avg Rating"