from django import forms
from.models import Movie

class MovieAddForm(forms.ModelForm):
    """add Movie form """
    class Meta:
        model = Movie
        fields = "__all__"
        exclude = ["slug"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "type": "text", "placeholder": "Název Filmu"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": "3"}),
            "release_date": forms.DateInput(attrs={"class": "form-control" ,"type": "date"}),
            "genres": forms.SelectMultiple(attrs={"class": "form-control", "type": "select"}),
            # "genres": forms.RadioSelect(attrs={"class": "form-control","cols":"2", "type": "radio"}),
            "actors": forms.SelectMultiple(attrs={"class": "form-control", "type": "select"}),
            "poster_image": forms.FileInput(attrs={"class": "form-control", "type": "file"}),
            "poster_url": forms.URLInput(attrs={"class": "form-control", "type": "url","placeholder": "https://.."}),

        }

        help_texts = {
            "title": "Zadej název filmu, slug si vytvoříme sami.",
            "description": "Tady zadej popis filmu.",
            "release_date": "Datum vydání filmu.",
            "genres": "Drž Ctrl a vyber požadované Žánry.",
            "actors": "Drž Ctrl a vyber požadované Herce.",
            "poster_image": "Pokud máš Poster Image, nahrej ho zde (nepovinné).",
            "poster_url": "Pokud máš Poster Image URL, Zadej ji zde (nepovinné).",
        }

        labels = {
            "title": "Název filmu",
            "description": "Popis filmu",
            "release_date": "Datum vydání",
            "genres": "Žánry",
            "actors": "Herci",
            "poster_image": "Obrázek (neovinné)",
            "poster_url": "URL Obrázku (nepovinné)",
        }
