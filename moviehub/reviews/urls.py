

from django.urls import path
from .views import add_review, edit_review

urlpatterns = [
    path('add-reviews/<int:movie_id>/', add_review, name="add_review"),
    path('edit-review/<int:pk>/', edit_review, name="edit_review"),
    # path('', func, name=""),

]