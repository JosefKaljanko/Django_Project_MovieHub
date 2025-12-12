from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.views import View
from movies.models import Movie, Actor, Genre
from reviews.forms import AddReviewForm, AddReviewForm2
from django.db.models import Avg
from django.contrib import messages   # login
from reviews.models import Review


class MovieListView(View):
    """Zobrazí seznam vsech filmů."""
    def get(self, request):
        movies = Movie.objects.all()
        category_menu = Genre.objects.all()
        context = {"movies": movies, "category_menu": category_menu}
        # return render(request, "movies/movie_list.html", {"movies": movies})
        return render(request, "movies/movie_list.html", context)
    def post(self, request):
        ...

class MovieDetailView(View):
    """zobrazí detail filmu a recenze"""

    def get(self, request, slug):
        movie = get_object_or_404(Movie, slug=slug)
        avg_rating = movie.reviews.aggregate(Avg('rating'))['rating__avg']

        user_review = None
        has_review = False
        if request.user.is_authenticated:
            user_review = Review.objects.filter(movie=movie, user=request.user).first()
            has_review = user_review is not None

        form = None
        if request.user.is_authenticated and not has_review:
            form = AddReviewForm2()

        context = {
            "movie": movie,
            "avg_rating": avg_rating,
            "form": form,
            "user_review": user_review,
            "has_review": has_review,

        }

        return render(request, "movies/movie_detail.html", context)

class GenreListView(View):
    def get(self, request):
        genres = Genre.objects.all()
        context = {"genres_list": genres}
        return render(request, "movies/genre_detail.html", context)
class GenreDetailView(View):
    def get(self, request, slug):
        genre = get_object_or_404(Genre.objects.prefetch_related("movies"), slug=slug)
        context = {"genre": genre, "movies": genre.movies.all()}
        return render(request, "movies/genre_detail.html", context)

