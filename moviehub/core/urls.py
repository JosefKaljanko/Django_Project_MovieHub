from django.urls import path
from .views import index
urlpatterns = [
    path("core/", index, name='index'),
]

