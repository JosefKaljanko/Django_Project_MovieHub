import pytest
from django.urls import reverse
from movies.models import Movie
from datetime import date


@pytest.mark.django_db
def test_movie_list_returns_200(client):
    """Movie list page returns HTTP 200."""
    url = reverse("all_movies")
    resp = client.get(url)
    assert resp.status_code == 200

@pytest.mark.django_db
def test_movie_list_pagination_page_2_returns_200(client):
    """Movie list pagination page 2 returns HTTP 200 when enough movies exist."""
    # vytvoř 13 filmů -> aby existovala 2. stránka při per_page=12
    for i in range(13):
        Movie.objects.create(
            title=f"Movie {i}",
            description="x",
            release_date=date(2024, 1, 1),
            # slug=f"movie-{i}",
        )
    url = reverse("all_movies")
    resp = client.get(url, {"page": 2})
    assert resp.status_code == 200