from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MovieViewSet, ReviewViewSet

router = DefaultRouter()
router.register("movies", MovieViewSet, basename="movie")
router.register("reviews", ReviewViewSet, basename="review")
urlpatterns = [
    path('', include(router.urls)),
]