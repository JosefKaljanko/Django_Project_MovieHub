from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError


class Genre(models.Model):
    """
    Model žánru filmu(akce, drama, komedie,...)
    """
    name = models.CharField(max_length=70)
    slug = models.SlugField(unique=True, blank=True, max_length=100, db_index=True)

    def clean(self):
        """pokud není slug - vygeneruje"""
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        """duplicity control"""
        if self.slug and Genre.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            raise ValidationError({"slug": f"Slug: '{self.slug}' already exists"})


    def save(self, *args, **kwargs):
        """field validation + clean()"""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Žánr"
        verbose_name_plural = "Žánry"



class Actor(models.Model):
    """
    Model herců
    """
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    bio = models.TextField(blank=True)

    def clean(self):
        """surname duplicity control"""
        if self.surname and Actor.objects.filter(surname = self.surname).exclude(pk=self.pk).exists():
            raise ValidationError({"surname": f"Surname: '{self.surname}' already exists"})

    def __str__(self):
        return f"{self.surname} {self.name}"

    class Meta:
        ordering = ["surname", "name"]
        verbose_name = "Herec"
        verbose_name_plural = "Herci"

class Movie(models.Model):
    """Model filmu"""
    title = models.CharField(max_length=100)
    description = models.TextField()
    release_date = models.DateField()
    slug = models.SlugField(unique=True, blank=True, max_length=125, db_index=True)
    genres = models.ManyToManyField(Genre, related_name="movies")
    actors = models.ManyToManyField(Actor,related_name="movies")
    poster_image = models.ImageField(upload_to="movie_posters", blank=True, null=True)
    poster_url = models.URLField(blank=True, null=True)

    def clean(self):
        """není slug - vygeneruje"""
        if not self.slug and self.title:
            self.slug = slugify(self.title)

        if self.slug and Movie.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            raise ValidationError({"slug": f"Slug: '{self.slug}' already exists"})

    @property
    def poster(self):
        """
        Jednotné pro template: movie.poster
        - když je upload -> vrací ImageField soubor (má .url)
        - jinak když je URL -> vrací string URL
        - jinak None
        """
        if self.poster_image:
            return self.poster_image
        if self.poster_url:
            return self.poster_url
        return None

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.release_date:%d-%m-%Y}"

    class Meta:
        ordering = ["-release_date", "title"]
        verbose_name = "Film"
        verbose_name_plural = "Filmy"