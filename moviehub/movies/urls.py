

from django.urls import path
from .views import (MovieListView,MovieDetailView, GenreListView, GenreDetailView)

urlpatterns = [
    path('movies/', MovieListView.as_view(), name="all_movies"),
    path('movie/<slug:slug>', MovieDetailView.as_view(), name="movie_detail"),
    path('genres/<slug:slug>', GenreDetailView.as_view(), name="genre_detail"),
    path('genres/', GenreListView.as_view(), name="genre"),
    # path('', func, name=""),

]