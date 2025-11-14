
from django.urls import path
from .views import home, about, author


urlpatterns = [
    path('', home, name="home_page"),
    path('about/', about, name="about_page"),
    path('about-author/', author, name="author_page"),
    # path('', func, name=""),

]