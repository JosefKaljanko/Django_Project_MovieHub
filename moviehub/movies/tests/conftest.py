from django.contrib.auth.models import User, Permission
import pytest


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="user",
        password="testpass123",
    )


@pytest.fixture
def editor(db):
    user = User.objects.create_user(
        username="editor",
        password="testpass123"
    )
    permission = Permission.objects.get(codename="add_movie")
    user.user_permissions.add(permission)
    return user

