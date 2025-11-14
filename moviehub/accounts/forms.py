
from django import forms
# login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.validators import EmailValidator


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Uživatelské Jméno:",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'},
                                   # render_value=False
                                   ),
        label="Heslo:",
        # strip=False,
    )

class CustomProfileEditForm(forms.ModelForm):
    username = forms.CharField(max_length=50,
                               widget=forms.TextInput(attrs={'class': 'form-control'}),
                               label="Uživatelské Jméno",
                               help_text="Zde zadejte vaše uživatelske jméno.")
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                             validators=[EmailValidator()],
                             help_text="Zde zadejte váš platný email.")

    bio = forms.CharField(widget=forms.Textarea(attrs={ 'class': 'form-control', 'rows': 4, "cols": 60}),
                          label="O vás:",
                          help_text="Zde zadejte stručný popis o vás.",

                          )

    class Meta:
        model = User
        fields = ('username', 'email', 'bio')
        template_name = 'accounts/profile_edit.html'
