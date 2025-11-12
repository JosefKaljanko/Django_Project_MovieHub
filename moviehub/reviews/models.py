from django.db import models

# Movie models from app movies
from movies.models import Movie

# User model from django...
from django.contrib.auth.models import User

# validator
from django.core.validators import MinValueValidator, MaxValueValidator



class Review(models.Model):
    """Model Recenze od uzivatele"""
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField(blank=False, validators=[MinValueValidator(1), MaxValueValidator(10)],help_text="Hodnocení 1-10")
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.movie.title} - {self.user.username} ({self.rating}/10)" #???

    class Meta:
        unique_together = ("movie", "user")
        ordering = ["-created_at"]
        verbose_name = "Recenze"
        verbose_name_plural = "Recenze"