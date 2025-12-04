from django import forms
# login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


from .models import UserProfile
from django.core.validators import EmailValidator

#original
# class CustomLoginForm(AuthenticationForm):
#     username = forms.CharField(
#         widget=forms.TextInput(attrs={'class': 'form-control'}),
#         label="Uživatelské Jméno:",
#     )
#     password = forms.CharField(
#         widget=forms.PasswordInput(attrs={'class': 'form-control'},
#                                    # render_value=False
#                                    ),
#         label="Heslo:",
#         # strip=False,
#     )

# -----> LOGIN FORM bootstrap <-----

class CustomLoginForm(AuthenticationForm):
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
    username = forms.CharField(
        max_length=50,
        label="Uživatelské Jméno",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'floatingUsername',
            "placeholder": "Username",
        }),
        # help_text="Zde zadejte vaše uživatelske jméno."
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
    # email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}),
    #                          validators=[EmailValidator()],
    #                          help_text="Zde zadejte váš platný email.")

    # BIO NENI V MODELU USER!!!
    # bio = forms.CharField(label="O vás:",
    #                       widget=forms.Textarea(attrs={
    #                           'class': 'form-control',
    #                           'id': 'floatingBio',
    #                           'rows': 4,
    #                           "cols": 60
    #                       }),
    #
    #                         help_text="Zde zadejte stručný popis o vás.",)

    class Meta:
        model = User
        fields = ('username', 'email')
        template_name = 'accounts/profile_edit.html'
        # skryje def dlouhy helptex od django username
        help_texts = {
            "username": ""
        }




# -----> EDIT PROF bio, avatar <-----
# TODO udelat upravu profilu username -> model:1; bio a avatar -> model:2
class CusProfEditForm(forms.ModelForm):

    # username = forms.CharField(max_length=50,
    #                            widget=forms.TextInput(attrs={'class': 'form-control', 'value': 'request.user'}),
    #                            label="Nové Uživatelské Jméno",
    #                            help_text="<br>Zde zadejte vaše uživatelske jméno. <br>")
    #
    bio = forms.CharField(
        label="O vás:",
        required=False,
        help_text="Zde zadejte stručný popis o vás.",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'id': 'floatingBio',
            'rows': 4,
            # "cols": 60
            "placeholder": "Napište něco o sobě...",
        }),
    )

    #
    #                       )
    #
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
        # alternativne
        # fields = ("bio", "avatar")