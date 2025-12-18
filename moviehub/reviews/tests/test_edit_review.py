import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
from movies.models import Movie
from reviews.models import Review

@pytest.mark.django_db
def test_edit_review_author_can_open(client):
    """Author can open edit review page."""
    user = User.objects.create_user(username="author", password="testpass123")
    client.login(username="author", password="testpass123")

    movie = Movie.objects.create(title="M3", description="d", release_date=date(2024, 1, 1), slug="m3")
    review = Review.objects.create(movie=movie, user=user, rating=7, comment="ok")

    resp = client.get(reverse("edit_review", kwargs={"pk": review.pk}))
    assert resp.status_code == 200

@pytest.mark.django_db
def test_edit_review_other_user_gets_404(client):
    """Non-author cannot edit someone else's review (404)."""
    author = User.objects.create_user(username="author2", password="testpass123")
    other = User.objects.create_user(username="other", password="testpass123")
    movie = Movie.objects.create(title="M4", description="d", release_date=date(2024, 1, 1), slug="m4")
    review = Review.objects.create(movie=movie, user=author, rating=9, comment="great")

    client.login(username="other", password="testpass123")
    resp = client.get(reverse("edit_review", kwargs={"pk": review.pk}))
    assert resp.status_code == 404