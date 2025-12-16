from django import forms
from .models import Review


class AddReviewForm(forms.ModelForm):
    """formular pro pridani recenze"""
    class Meta:
        model = Review
        fields = ["rating", "comment"]

        #widgets pro definovani attributu v html!!!
        # v html {{ form.as_p }} = <p></p> _as_h1....

        # widgets = {
        #     "rating": forms.RadioSelect(),
        #     "rating": forms.NumberInput(attrs={"class": "review-form","min": 0, "max": 10}),
        #     "comment": forms.Textarea(attrs={"class": "review-form","rows": 3, "cols": 50}),
        # }

# add_review.html
class AddReviewForm2(forms.ModelForm):
    """ACTIVE formular pro pridani recenze"""
    class Meta:
        model = Review
        fields = ["rating", "comment"]

        #widgets pro definovani attributu v html!!!
        # v html {{ form.as_p }} = <p></p> _as_h1....

        widgets = {
            # "rating": forms.RadioSelect(),
            "rating": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "1-10",
                    "min": 1,
                    "max": 10,
                    "step": 1,
                }
            ),
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Napiš komentář...",
                    "rows": 3,
                    "cols": 50,
                }
            ),
        }
        labels= {
            "rating": "Rating",
            "comment": "Comment",
        }


