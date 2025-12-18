from django.contrib.auth.models import User
import pytest



@pytest.fixture
def user(db):
    """Vytvoří testovacího uživatele."""
    return User.objects.create_user(
        username="user1",
        password="testpass123",
        email="user1@test.cz"
    )

