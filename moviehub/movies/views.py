from random import random, choice, choices

from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.views import View
from pygments.lexers import q

from movies.models import Movie, Actor, Genre
from reviews.forms import AddReviewForm, AddReviewForm2
from django.db.models import Avg
from django.contrib import messages   # login
from reviews.models import Review


class MovieListView(View):
    """Zobrazí seznam vsech filmů."""
    def get(self, request):
        # movies = Movie.objects.all()
        q = request.GET.get("q", "").strip()
        movies = (
            Movie.objects.all()
            .prefetch_related('genres')
            .annotate(avg_rating=Avg('reviews__rating'))
            .order_by('-id')
        )

        if q:
            movies = movies.filter(title__icontains=q)


        category_menu = Genre.objects.all()
        context = {
            "movies": movies,
            "category_menu": category_menu,
            "q": q,
        }
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

    # def post(self, request, slug):
    #     movie = get_object_or_404(Movie, slug=slug)
    #     form = AddReviewForm2(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect("movie_detail", slug=slug)
    #     return render(request, "movies/movie_detail.html", {"form": form})

class GenreListView(View):
    def get(self, request):
        genres = Genre.objects.all()
        random_button = request.GET.get("random_genre")

        if random_button == "random":
            genre = choice(genres)
            return redirect("genre_detail", slug=genre.slug)

        context = {"genres_list": genres,
                   # "genre": genre,
                   }
        return render(request, "movies/genre_detail.html", context)


class GenreDetailView(View):
    def get(self, request, slug):
        genre = get_object_or_404(Genre.objects.prefetch_related("movies"), slug=slug)
        genres_list = Genre.objects.all()
        context = {"genre": genre, "movies": genre.movies.all(), "genres_list": genres_list}
        return render(request, "movies/genre_detail.html", context)

