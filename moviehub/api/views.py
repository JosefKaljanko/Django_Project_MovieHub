from django.shortcuts import render
from rest_framework import viewsets

from movies.models import Movie
from .serializers import MovieSerializer


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read only API pro filmy
    """
    queryset = (
        Movie.objects
        .all()
        .prefetch_related("reviews")
    )
    serializer_class = MovieSerializer
    # pokud api/movies/<slug>/  misto id
    lookup_field = "slug"

