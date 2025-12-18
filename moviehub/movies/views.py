from random import random, choice, choices

from django.db.models.functions import Coalesce
from django.forms import BaseForm
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from movies.models import Movie, Actor, Genre
from reviews.forms import AddReviewForm, AddReviewForm2
from django.db.models import Avg, Count, Value, FloatField
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from reviews.models import Review

from django.core.paginator import Paginator
from .forms import MovieAddForm


def get_top_movies(limit=10):
    """Top 10 filmů podle průměrného ratingu (bez hodnocení = 0.0)"""
    return (
        Movie.objects
        .annotate(avg_rating=Coalesce(Avg("reviews__rating"), Value(0.0), output_field=FloatField()))
        .order_by("-avg_rating", "-id")[:limit]
    )


class MovieListView(View):
    """Zobrazí seznam vsech filmů."""
    def get(self, request):
        # movies = Movie.objects.all()
        q = request.GET.get("q", "").strip()

        # paginator _qs= queryset
        page_number = request.GET.get("page", 1)
        # misto movies movies_qs
        movies_qs = (
            Movie.objects.all()
            .prefetch_related('genres')
            .annotate(avg_rating=Avg('reviews__rating'))
            .order_by('-id')
        )

        movies = (
            Movie.objects.all()
            .prefetch_related('genres')
            .annotate(avg_rating=Avg('reviews__rating'))
            .order_by('-id')
        )

        if q:
            # movies = movies.filter(title__icontains=q)
            movies_qs = movies_qs.filter(title__icontains=q)

        paginator = Paginator(movies_qs, 9)
        page_obj = paginator.get_page(page_number)

        category_menu = Genre.objects.all()
        context = {
            # "movies": movies, # ---> ZRUSIT
            "movies": page_obj.object_list, # volitelné
            "page_obj": page_obj,
            "paginator": paginator,
            "category_menu": category_menu,
            "q": q,
            "top_movies": get_top_movies(10),
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
        genres = (
            Genre.objects
            .annotate(movie_count=Count("movies"))
            .order_by("-movie_count", "name")
        )

        genres_with_mov = (
            Genre.objects
            .annotate(movie_count=Count("movies"))
            .filter(movie_count__gt=0)
        )

        random_button = request.GET.get("random_genre")
        if random_button == "random":
            genre = choice(genres_with_mov)
            return redirect("genre_detail", slug=genre.slug)

        context = {"genres_list": genres,
                   "top_movies": get_top_movies(10),
                   # "genre": genre,
                   }
        return render(request, "movies/genre_detail.html", context)


class GenreDetailView(View):
    def get(self, request, slug):
        genre = get_object_or_404(Genre.objects.prefetch_related("movies"), slug=slug)

        genres_list = (
            Genre.objects
            .annotate(movie_count=Count("movies"))
            .order_by("-movie_count", "name")
        )

        context = {
            "genre": genre,
            "movies": genre.movies.all(),
            "genres_list": genres_list,
            "top_movies": get_top_movies(10),
        }
        return render(request, "movies/genre_detail.html", context)


class AddMovieView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Movie
    form_class = MovieAddForm
    template_name = "movies/add_movie.html"
    permission_required = "movies.add_movie"
    # permission_denied_message = "Nemáš oprávnění přidávat Filmy..."
    # raise_exception = False
    # login_url = reverse_lazy("/all_movies/")
    # success_url = reverse_lazy("all_movies")

    def get_success_url(self):
        return reverse_lazy("movie_detail", kwargs={"slug": self.object.slug})

    def handle_no_permission(self):
        messages.warning(self.request,
                         "Nemáš oprávnění přidávat Filmy..."
                         )
        return redirect("all_movies")

