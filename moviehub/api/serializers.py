# api serializers
from django.template.context_processors import request
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from movies.models import Movie
from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    movie = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all()
    )

    class Meta:
        model = Review
        fields = [
            "id",
            "user",
            "movie",
            "rating",
            "comment",
            "created_at",
        ]
        read_only_fields = ["id", "user", "created_at"]

    def validate_rating(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError("Hodnocení musí být 1 - 10")
        return value

    def validate(self, attrs):
        """
        Kontrola 1 user = 1 recenze
        """
        request = self.context.get("request")
        print(request.user)
        print("attrs: ", attrs)
        user = getattr(request,"user", None)
        print("user: ", user)
        movie = attrs.get("movie")

        if user is None or not user.is_authenticated:
            raise serializers.ValidationError(
                "Pro vytvoření recenze se musíš přihlásit"
            )

        # Create vs Update:
        # - při create self.instance == None
        # - při update self.instance je už existující Review
        qs = Review.objects.filter(user=user, movie=movie)
        if self.instance is not None:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError(
                "Pro tento film už máš recenzi."
            )
        return attrs

class MovieSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "release_date",
            "poster_url",
            "poster_image",
            "reviews",
            "actors",
            "genres",
        ]


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "movie", "rating", "comment"]
        read_only_fields = ["id"]

    def validate(self, attrs):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        movie = attrs.get("movie")

        if user is None or not user.is_authenticated:
            raise serializers.ValidationError(
                "pro vytvoření recenze se musíš přihlásit."
            )

        # 1 user = 1recenze
        if Review.objects.filter(user=user, movie=movie).exists():
            raise serializers.ValidationError(
                "Pro tento film už máš recenzi."
            )

        return attrs

    # 4 konec