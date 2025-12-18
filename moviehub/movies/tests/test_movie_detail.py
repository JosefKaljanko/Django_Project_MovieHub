import pytest
from django.urls import reverse
from movies.models import Movie
from datetime import date

@pytest.mark.django_db
def test_movie_detail_existing_returns_200(client):
    """Movie detail for existing movie returns HTTP 200."""
    movie = Movie.objects.create(
        title="Detail Movie",
        description="desc",
        release_date=date(2024, 1, 1),
        slug="detail-movie",
    )
    resp = client.get(reverse("movie_detail", kwargs={"slug": movie.slug}))
    assert resp.status_code == 200

@pytest.mark.django_db
def test_movie_detail_nonexistent_returns_404(client):
    """Movie detail for missing movie returns HTTP 404."""
    resp = client.get(reverse("movie_detail", kwargs={"slug": "nope-nope"}))
    assert resp.status_code == 404