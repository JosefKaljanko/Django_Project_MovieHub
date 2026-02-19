from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter

from movies.models import Movie
from reviews.models import Review

from .serializers import (MovieSerializer,
                          ReviewSerializer,
                          ReviewCreateSerializer,
                          )


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read only API pro filmy
    - GET /api/movies/
    - GET /api/movies/<id>/
    + Vyhledávání, filtrování podle roku, řazení
    """
    queryset = (
        Movie.objects.all()
        .prefetch_related("reviews")
    )
    serializer_class = MovieSerializer
    # pokud api/movies/<slug>/  misto id
    # lookup_field = "slug"

    # Vyhledáváni pres ?search=... pres icntains
    search_fields = ["title", "description"]

    # řazení přes ?ordering=release_year nebo ?ordering=-release_year
    ordering_fields = ["release_date" "created_at"]
    ordering = ["-release_date"]
    # filter_backends = (SearchFilter, OrderingFilter)

    def get_queryset(self):
        """
        filtr podle roku:
        /api/movies/?year=1999
        """
        qs = Movie.objects.all().prefetch_related("reviews")

        year = self.request.query_params.get("year")
        if year:
            qs = qs.filter(release_date__year=year)

        return qs


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Povolí čtení všem, ale úpravy jen Autorovi recenze
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class ReviewViewSet(viewsets.ModelViewSet):
    """
    API pro recenze:
    - GET /api/reviews/ (list)
    - GET /api/reviews/<id>/ (detail)
    - POST /api/reviews/ (create)
    - PUT/PATCH/DELETE jen Autor
    """
    queryset = Review.objects.select_related("movie", "user")
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        # pro create/updasate pouzivame write serializer
        if self.action == ["create", "update", "partial_update"]:
            return ReviewCreateSerializer
        return ReviewSerializer

    def perform_create(self, serializer):
        # user z requestu, movie + rating + comment z dat
        serializer.save(user=self.request.user)
