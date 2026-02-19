from django.db import models
from django.db.models import Avg, Count, Value, FloatField
from django.db.models.functions.comparison import Coalesce


class MovieQuerySet(models.QuerySet):
    def with_avg_rating(self,*args,**kwargs):
        """
        Vrátí queryset s anotovaným průměrným hodnocením a počtem recenzí.
        každý Movie objekt pak má:
          - movie.avg_rating
          - movie.reviews_count
        """

        return self.annotate(
            avg_rating=Avg("reviews__rating"),
            reviews_count=Count("reviews", distinct=True)
        )

    def with_avg_rating_zero(self):
        """
        přidá k filmům průměrné hodnocení kde None -> 0.0
        Určeno pro žebříčky (top filmy)
        """
        return self.annotate(
            avg_rating=Coalesce(
                Avg("reviews__rating"),
                Value(0.0),
                output_field=FloatField()
            ),
            reviews_count=Count("reviews", distinct=True)
        )

    def top_rated(self, limit=10, include_unrated=True):
        """
        Vrátí top N filmů podle průměrného hodnocení.
            • include_unrated=True  -> filmy bez recenzí mají 0.0
            • include_unrated=False -> filmy bez recenzí se vyhodí
        """
        qs = self.with_avg_rating_zero()

        if not include_unrated:
            qs = qs.filter(reviews__isnull=False)

        return qs.order_by("-avg_rating", "-id")[:limit]

    def search(self,q: str | None):
        """
        Jednoduché vyhledávání podle názvu.
        pokud q je None vrací půlvodní queryset.
        """
        if not q:
            return self
        return self.filter(title__icontains=q.strip())


    def order_default(self):
        """
        Výchozí řazení filmů (nejnovější podle id první)
        """
        return self.order_by('-id')

class GenreQuerySet(models.QuerySet):
    def with_movie_count(self):
        """
        Vrátí počet filmů v žánru
        """
        return self.annotate(movie_count=Count("movies", distinct=True))

    def with_movies_only(self):
        """
        Vrátí žánry kde jsou filmy
        """
        return self.with_movie_count().filter(movie_count__gt=0)