# api serializers

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from movies.models import Movie
from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "user",
            "rating",
            "comment",
            "created_at",
        ]

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
            # "created_at",
            # "updated_at",
            "reviews",            
        ]