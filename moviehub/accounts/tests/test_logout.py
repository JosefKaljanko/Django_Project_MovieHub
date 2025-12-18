import pytest
from django.urls import reverse



@pytest.mark.django_db
def test_logout_requires_login(client):
    """Nepřihlášený uživatel je při logoutu přesměrován."""
    response = client.get(reverse("logout"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_logout_logged_user_redirects_and_logs_out(client, user):
    """Přihlášený uživatel je odhlášen a přesměrován."""
    client.login(username=user.username, password="testpass123")

    response = client.get(reverse("logout"))

    assert response.status_code == 302
    # session po logoutu už nesmí obsahovat user id
    assert "_auth_user_id" not in client.session