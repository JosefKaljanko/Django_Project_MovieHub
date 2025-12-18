import pytest
from django.urls import reverse
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_register_get_returns_200(client):
    """GET na register stránku vrátí 200."""
    resp = client.get(reverse("register"))
    assert resp.status_code == 200


@pytest.mark.django_db
def test_register_post_creates_user_and_redirects(client):
    """POST registrace vytvoří uživatele a přesměruje (a uživatel je přihlášen)."""
    resp = client.post(
        reverse("register"),
        {
            "username": "newuser",
            "email": "newuser@test.cz",
            "password": "testpass123",
            "password2": "testpass123",
        },
    )

    assert resp.status_code == 302
    assert User.objects.filter(username="newuser").exists()

    # bonus: ověření, že je user přihlášen (session obsahuje _auth_user_id)
    assert "_auth_user_id" in client.session