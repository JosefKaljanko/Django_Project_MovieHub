import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
from movies.models import Movie
from reviews.models import Review

@pytest.mark.django_db
def test_add_review_requires_login(client):
    """Add review requires authentication (redirects when anonymous)."""
    movie = Movie.objects.create(
        title="R Movie",
        description="desc",
        release_date=date(2024, 1, 1),
        slug="r-movie",
    )
    resp = client.get(reverse("add_review", kwargs={"movie_id": movie.id}))
    assert resp.status_code == 302  # redirect na login

@pytest.mark.django_db
def test_add_review_creates_review_for_logged_user(client):
    """Logged user can create a review and is redirected."""
    user = User.objects.create_user(username="u1", password="testpass123")
    client.login(username="u1", password="testpass123")

    movie = Movie.objects.create(
        title="R2 Movie",
        description="desc",
        release_date=date(2024, 1, 1),
        slug="r2-movie",
    )

    resp = client.post(
        reverse("add_review", kwargs={"movie_id": movie.id}),
        {"rating": 8, "comment": "Nice"},
    )
    assert resp.status_code == 302
    assert Review.objects.filter(movie=movie, user=user).exists()