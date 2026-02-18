from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Aggregate
from django.contrib import messages
from .forms import AddReviewForm2
from .models import Review
from movies.models import Movie


@login_required
def add_review(request, movie_id):
    """Pridani recenze od uživatele k filmu. 1 uzivatel=1 recenze"""
    movie = get_object_or_404(Movie, pk=movie_id)
    avg_rating = movie.reviews.aggregate(Avg('rating'))['rating__avg']


    existing_review = Review.objects.filter(movie=movie, user=request.user).exists()
    if existing_review:
        messages.warning(request, "Tento film jsi již hodnotil. Recenzi můžeš upravit.")
        return redirect("movie_detail", slug=movie.slug)

    if request.method == "POST":
        form = AddReviewForm2(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()        # POVOVLIT SAVE !!!!
            messages.success(request, "Díki za recenzi!")
            return redirect("movie_detail", slug=movie.slug)
    else:
        form = AddReviewForm2()

        context = {
            "form": form,
            "movie": movie,
            "avg_rating": avg_rating
        }
        return render(request, "reviews/add_review.html", context)
    return render(request, "reviews/add_review.html", {"form": form, "movie": movie, "avg_rating": avg_rating})

@login_required
def edit_review(request, pk=None):
    """Edit reviews = jen Autor"""
    review = get_object_or_404(Review, pk=pk, user=request.user)

    if request.method == "POST":
        form = AddReviewForm2(request.POST, instance=review)
        if form.is_valid() and form.has_changed():
            form.save()
            messages.success(request, "Recenze byla upravena.")
            return redirect("movie_detail", slug=review.movie.slug)
    else:
        form = AddReviewForm2(instance=review)

    context = {
        "form": form,
        "review": review,
        "movie": review.movie,
    }
    return render(request,"reviews/edit_review.html", context)

