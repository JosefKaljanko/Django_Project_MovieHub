import pytest
from django.urls import reverse
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_profile_requires_login(client):
    """Nepřihlášený uživatel je přesměrován z profilu."""
    response = client.get(reverse("profile"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_profile_logged_user_ok(client, user):
    """Přihlášený uživatel vidí svůj profil."""
    client.login(username=user.username, password="testpass123")
    response = client.get(reverse("profile"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_profile_edit_requires_login(client):
    """Nepřihlášený uživatel nemůže editovat profil."""
    response = client.get(reverse("profile_edit"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_profile_edit_extra_logged_user_ok(client, user):
    """Přihlášený uživatel může editovat rozšířený profil."""
    client.login(username=user.username, password="testpass123")
    response = client.get(reverse("profile_edit_extra"))
    assert response.status_code == 200