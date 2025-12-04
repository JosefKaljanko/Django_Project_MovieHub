from os.path import altsep

from django import forms
# login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.template.context_processors import request

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
# bootstrap
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control w-75',
            'id': 'floatingUsername',
            "placeholder": "Username"}), # musi byt pro bootstrap
        label="Uživatelské Jméno:",
        # label="username",
    )
    password = forms.CharField(
        label="Heslo:",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'floatingPassword',
            "placeholder": "Password", # musí být pro bootstrap!!!
        },
                                   # render_value=False
                                   ),
        # strip=False,
    )

class CustomProfileEditForm(forms.ModelForm):
    username = forms.CharField(max_length=50,
                               label="Uživatelské Jméno",
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'id': 'floatingUsername',
                                   "placeholder": "Username",
                               }),

                               help_text="Zde zadejte vaše uživatelske jméno.")
    # email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}),
    #                          validators=[EmailValidator()],
    #                          help_text="Zde zadejte váš platný email.")

    bio = forms.CharField(label="O vás:",
                          widget=forms.Textarea(attrs={
                              'class': 'form-control',
                              'id': 'floatingBio',
                              'rows': 4,
                              "cols": 60
                          }),

                            help_text="Zde zadejte stručný popis o vás.",)

    class Meta:
        model = User
        fields = ('username', 'email', 'bio')
        template_name = 'accounts/profile_edit.html'





# TODO udelat upravu profilu username -> model:1; bio a avatar -> model:2
class CusProfEditForm(forms.ModelForm):

    username = forms.CharField(max_length=50,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'value': 'request.user'}),
                               label="Nové Uživatelské Jméno",
                               help_text="<br>Zde zadejte vaše uživatelske jméno. <br>")
    #
    # bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, "cols": 60}),
    #                       label="O vás:",
    #                       help_text="Zde zadejte stručný popis o vás.",
    #
    #                       )
    #
    avatar2 = forms.ImageField(required=False, label="Obrázek",
                               widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserProfile
        # exclude = ('user',)
        fields = '__all__'