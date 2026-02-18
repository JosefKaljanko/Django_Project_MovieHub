from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile



class CustomLoginForm(AuthenticationForm):
    """login form"""
    username = forms.CharField(
        label="Uživatelské Jméno:",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'floatingUsername',
            "placeholder": "Uživatelské Jméno:",  # musi byt pro bootstrap
            "autocomplete": "username",
        }),
    )
    password = forms.CharField(
        label="Heslo:",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'floatingPassword',
            "placeholder": "Password", # musí být pro bootstrap!!!
            "autocomplete": "current-password",
        }),
    )

# -----> EDIT USER (username, email) <-----

class CustomProfileEditForm(forms.ModelForm):
    """edit form"""
    username = forms.CharField(
        max_length=50,
        label="Uživatelské Jméno",
        help_text="Zde zadejte vaše uživatelske jméno.",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'floatingUsername',
            "placeholder": "Username",
        }),
    )

    email = forms.EmailField(
        label="Email",
        required=False,
        help_text="Zadejte platný Email (Volitelné).",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "id": "floatingEmail",
            "placeholder": "name@example.com",
        }),
    )

    class Meta:
        model = User
        fields = ('username', 'email')
        template_name = 'accounts/profile_edit.html'
        # skryje def dlouhy helptex od django username
        help_texts = {
            "username": ""
        }




# -----> EDIT PROF bio, avatar <-----
class CusProfEditForm(forms.ModelForm):
    """edit form bio/avatar"""
    bio = forms.CharField(
        label="O vás:",
        required=False,
        help_text="Zde zadejte stručný popis o vás.",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'id': 'floatingBio',
            'rows': 4,
            "placeholder": "Napište něco o sobě...",
        }),
    )


    avatar = forms.ImageField(
        required=False,
        label="Profilový Obrázek",
        widget=forms.FileInput(attrs={
            'class': 'form-control'
        }),
    )

    class Meta:
        model = UserProfile
        exclude = ('user',)