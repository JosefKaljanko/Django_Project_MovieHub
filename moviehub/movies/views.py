from .forms import MovieAddForm
from .models import Movie, Genre
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Value, FloatField  # avg count
from django.db.models.functions import Coalesce
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
# from movies.models import Movie, Genre
from random import choice
from reviews.forms import AddReviewForm2
from reviews.models import Review


def get_top_movies(limit=10, unrated=True):
    """Top 10 filmů podle průměrného ratingu (bez hodnocení = 0.0)"""
    # print("HERE: ",Movie.objects.with_avg_rating())
    # print("HERE2: ",Movie.objects.values("title").annotate(avg_rating=Coalesce(Avg("reviews__rating"), Value(0.0), output_field=FloatField())).order_by("-avg_rating")[:limit])
    # print("HERE3: ",Movie.objects.top_rated(include_unrated=True, limit=20).values("title","avg_rating"))
    return Movie.objects.top_rated(limit=limit, include_unrated=unrated)



class MovieListView(View):
    """Zobrazí seznam vsech filmů. (grid + pagination)"""
    def get(self, request):
        """
        Vrátí stranku se seznamem všechfilmů (grid + pagination).
        """
        q = request.GET.get("q", "").strip()
        page_number = request.GET.get("page", 1)

        movies_qs = (
            Movie.objects   # Movie.objects.all()
            .search(q)      # movies_qs.filter(title__icontains=q)
            .prefetch_related("genres", "actors")
            .with_avg_rating()
            .order_default()
        )
        # movies_qs = Movie.objects.all()
        # if q:
        #     movies_qs = movies_qs.filter(title__icontains=q)

        # movies_qs = (
        #     movies_qs
            # .prefetch_related('genres', 'actors')
            # .annotate(avg_rating=Avg('reviews__rating'),
            #           reviews_count=Count("reviews",distinct=True))
            # .order_by('-id')
        # )

        print(movies_qs.values("title", "avg_rating","genres", "reviews_count"))

        paginator = Paginator(movies_qs, 9)
        page_obj = paginator.get_page(page_number)
        category_menu = Genre.objects.all()

        context = {
            "movies": page_obj.object_list, # volitelné
            "page_obj": page_obj,
            "paginator": paginator,
            "category_menu": category_menu,
            "q": q,
            "top_movies": get_top_movies(limit=10),
        }
        return render(request, "movies/movie_list.html", context)



    def post(self, request):
        """Zatím Neaktivni"""
        ...

class MovieDetailView(View):
    """zobrazí detail filmu a recenze"""

    def get(self, request, slug):
        """
        Vrátí stranku detailu filmu;
        login => form (pokud nema review)
        form se odesila na jiny view (add_review)
        """
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
    """
    view = seznam žánrů + počet filmů
    random žánr...
    """
    def get(self, request):
        """
        vrátí seznam žánrů nebo přesměruje na nahodny
        """
        genres = (
            Genre.objects
            .with_movie_count()
            # .annotate(movie_count=Count("movies"))
            .order_by("-movie_count", "name")
        )

        genres_with_mov = Genre.objects.with_movies_only()

        random_button = request.GET.get("random_genre")
        if random_button == "random" and genres_with_mov.exists():
            genre = choice(list(genres_with_mov))
            return redirect("genre_detail", slug=genre.slug)

        context = {"genres_list": genres,
                   "top_movies": get_top_movies(10),
                   }
        return render(request, "movies/genre_detail.html", context)


class GenreDetailView(View):
    """
    Zobrazí • detail žánru
            • filmy v něm
            • seznam všech žánrů

    """
    def get(self, request, slug):
        """vratí stranku detailu žánru a filmů v něm"""
        genre = get_object_or_404(Genre.objects.prefetch_related("movies"), slug=slug)

        genres_list = (
            Genre.objects
            .with_movie_count()
            # .annotate(movie_count=Count("movies"))
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
    """View pro vytvoření filmu, jen s oprávněním movies.add_movie"""
    model = Movie
    form_class = MovieAddForm
    template_name = "movies/add_movie.html"
    permission_required = "movies.add_movie"

    def get_success_url(self):
        """po vytvoření redirect na detail noveho filmu"""
        return reverse_lazy("movie_detail", kwargs={"slug": self.object.slug})

    def handle_no_permission(self):
        """při chybě presmeruje a varuje uživatele"""
        messages.warning(self.request,
                         "Nemáš oprávnění přidávat Filmy..."
                         )
        return redirect("all_movies")

