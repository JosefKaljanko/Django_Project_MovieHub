from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.views import View
from movies.models import Movie, Actor, Genre
from reviews.forms import AddReviewForm
from django.contrib import messages   # login


class MovieListView(View):
    """Zobrazí seznam vsech filmů."""
    def get(self, request):
        movies = Movie.objects.all()
        return render(request, "movies/movie_list.html", {"movies": movies})
    def post(self, request):
        ...

class MovieDetailView(View):
    """zobrazí detail filmu a recenze"""
    def get(self, request, slug):
        movie = get_object_or_404(Movie, slug=slug)
        form = AddReviewForm()
        return render(request, "movies/movie_detail.html", {"movie": movie, "form": form})

class GenreListView(View):
    def get(self, request):
        genres = get_list_or_404(Genre.objects.all())
        context = {"genres_list": genres}
        return render(request, "movies/genre_detail.html", context)
class GenreDetailView(View):
    def get(self, request, slug):
        genre = get_object_or_404(Genre.objects.prefetch_related("movies"), slug=slug)
        context = {"genre": genre, "movies": genre.movies.all()}
        return render(request, "movies/genre_detail.html", context)

