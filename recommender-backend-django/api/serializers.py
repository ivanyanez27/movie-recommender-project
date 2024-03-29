from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import ApiMovie, ApiRating, ApiRecommender
from django.contrib.auth.models import User


# Movie Serializer
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiMovie
        fields = ('id', 'title', 'genre', 'no_of_ratings', 'avg_rating')


# Rating Serializer
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiRating
        fields = ('id', 'rating', 'user', 'movie')


# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    # Create a user
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        token = Token.objects.create(user=user)
        return user


class RecommenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiRecommender
        fields = ('user', 'recommendations', 'title')

