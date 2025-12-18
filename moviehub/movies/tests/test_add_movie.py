import pytest
from django.urls import reverse

from movies.models import Movie, Genre, Actor


@pytest.mark.django_db
def test_movie_list_view_200(client):
    response = client.get(reverse("all_movies"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_without_permission_cannot_add_movie(client, user):
    # user = User.objects.create_user(
    #     username="user1",
    #     password="testpass123"
    # )

    client.login(username=user.username, password="testpass123")

    response = client.get(reverse("add_movie"))

    assert response.status_code in (302, 403)


@pytest.mark.django_db
def test_user_with_permission_can_add_movie(client, editor):
    client.login(username=editor.username, password="testpass123")
    genre = Genre.objects.create(name="Action", slug="action")
    actor = Actor.objects.create(name="Test", surname="Actor")


    response = client.post(
        reverse("add_movie"),
        {
            "title": "Test_Title_From_Test",
            "description": "Test_Description_From_Test",
            "release_date": "2024-01-01",
            "genres": [genre.pk],
            "actors": [actor.pk],
        }
    )

    if response.status_code == 200:
        form = response.context["form"]
        assert False, f"Form invalid: {form.errors}"

    assert response.status_code == 302
    #
    assert Movie.objects.filter(title="Test_Title_From_Test").exists()

    movie = Movie.objects.get(title="Test_Title_From_Test")
    assert response["Location"] == reverse("movie_detail", kwargs={"slug": movie.slug})




