from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from .models import ApiMovie, ApiRating, ApiRecommender
from .serializers import MovieSerializer, RatingSerializer, UserSerializer, RecommenderSerializer
from .hybrid_recommender import CollaborativeFiltering, ContentBasedFiltering
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny


# User view
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


# Recommender view
class RecommenderViewSet(viewsets.ModelViewSet):
    queryset = ApiRecommender.objects.all()
    serializer_class = RecommenderSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    @action(detail=True, methods=['GET'])
    def get_user_recommendations(self, request, pk=None):
        # Get the users recommendations
        user = request.user
        recommendations = ApiRecommender.objects.filter(user=user.id)

        # Get the id's of each movie
        recommendation_ids = []
        for obj in recommendations:
            recommendation_ids.append(obj.recommendations_id)

        # Query the user's movies and return the queryset
        movies = ApiMovie.objects.filter(id__in=recommendation_ids)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def get_recommendations(self, request, pk=None):
        # if 'id' in request.data:
        user = request.user
        recommendations = []

        # Remove user's current recommendations, and create new ones
        ApiRecommender.objects.filter(user=user.id).delete()

        # Get collaborative recommendations
        cbf = CollaborativeFiltering(int(pk))
        cbf.processData()
        if len(cbf.user_history) > 0:
            cbf.getSimilarUsers()
            cbf.recommend()
            recommendations += cbf.recommendations

        # Get content based recommendations
        cnf = ContentBasedFiltering(int(pk))
        cnf.processData()
        if len(cnf.user_history) > 0:
            cnf.getSimilarity()
            cnf.recommend()
            recommendations += cnf.recommendations

        # Movies created and added to database
        for movieId in recommendations:
            if len(recommendations) > 0:
                movie = ApiMovie.objects.get(id=movieId)
                recommended = ApiRecommender.objects.create(user=user, recommendations=movie, title=movie.title)
                recommended.save()

        response = {'message': 'Recommendations processed'}
        return Response(response, status=status.HTTP_200_OK)


# Movie view
class MovieViewSet(viewsets.ModelViewSet):
    queryset = ApiMovie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        if 'stars' in request.data:
            movie = ApiMovie.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user
            # if movie rating is created already
            try:
                rating = ApiRating.objects.get(user=user.id, movie=movie.id)
                rating.rating = stars
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'Rating updated', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                rating = ApiRating.objects.create(user=user, movie=movie, rating=stars)
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'Rating created', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'you need to give ratings'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


# Rating view
class RatingViewSet(viewsets.ModelViewSet):
    queryset = ApiRating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # Override update method
    def update(self, request, *args, **kwargs):
        response = {'message': 'Ratings cannot be updated'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # Override create method
    def create(self, request, *args, **kwargs):
        response = {'message': 'Ratings cannot be created'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
