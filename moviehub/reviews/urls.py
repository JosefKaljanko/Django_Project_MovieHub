

from django.urls import path
from .views import add_review

urlpatterns = [
    path('add-reviews/<int:movie_id>/', add_review, name="add_review"),
    # path('', func, name=""),

]