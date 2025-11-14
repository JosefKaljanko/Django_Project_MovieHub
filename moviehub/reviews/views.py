from django.shortcuts import render, get_object_or_404, redirect
from .forms import AddReviewForm
from movies.models import Movie
from accounts.models import User
from django.contrib.auth.decorators import login_required


@login_required
def add_review(request, movie_id):
    """pridani recenze"""
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == "POST":
        form = AddReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            # review.save()        # POVOVLIT SAVE !!!!
            return redirect("movie_detail", slug=movie.slug)
    else:
        form = AddReviewForm()
        return render(request, "reviews/add_review.html", {"form": form, "movie": movie})
    return render(request, "reviews/add_review.html", {"form": form, "movie": movie})