from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from .models import ApiMovie, ApiRating
from .serializers import MovieSerializer, RatingSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny


# User view
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


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
