from profile import Profile
from django.urls import path
from .views import (logout_view, RegisterView, profile,CustomProfileEdit, CustomProfileEdit2)
from django.contrib.auth.views import LoginView, LogoutView, UserModel
from .forms import CustomLoginForm,CustomProfileEditForm

urlpatterns = [
    path('accounts/register/', RegisterView.as_view(), name="register"),
    path('accounts/logout/', logout_view, name="logout"),
    path('accounts/login/', LoginView.as_view(template_name='accounts/login.html', authentication_form=CustomLoginForm), name="login"),
    path('accounts/profile/', profile, name="profile"),
    path('accounts/profile/edit/', CustomProfileEdit.as_view(), name="profile_edit"),
    path('accounts/profile/edit-extra/', CustomProfileEdit2.as_view(), name="profile_edit_extra"),
]