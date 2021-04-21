import pandas as pd
from scipy.stats import pearsonr
from itertools import combinations
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from .models import ApiMovie, ApiRating


class RecommenderBase:
    def __init__(self, uid):
        self.userId = uid
        self.movies = []
        self.ratings = []
        self.querysetToDataframe()

    # Turn queryset information into dataframes
    def querysetToDataframe(self):
        title_list = list(ApiMovie.objects.values_list('title', flat=True))
        genre_list = list(ApiMovie.objects.values_list('genre', flat=True))
        movieId_list = list(ApiMovie.objects.values_list('id', flat=True))

        movie_data = {'title': title_list,
                      'genre': genre_list,
                      'movieId': movieId_list}

        self.movies = pd.DataFrame(movie_data, columns=['movieId', 'title', 'genre'])

        # Turn ratings into dataframe
        rating_list = list(ApiRating.objects.values_list('rating', flat=True))
        rating_list = [float(x) for x in rating_list]
        rmovieId_list = list(ApiRating.objects.values_list('movie_id', flat=True))
        userId_list = list(ApiRating.objects.values_list('user_id', flat=True))

        rating_data = {'rating': rating_list,
                       'movieId': rmovieId_list,
                       'userId': userId_list}

        self.ratings = pd.DataFrame(rating_data, columns=['userId', 'movieId', 'rating'])


# Collaborative Filtering Recommender
class CollaborativeFiltering(RecommenderBase):
    def __init__(self, uid):
        super().__init__(uid)
        self.user_history = []
        self.similar_users = pd.DataFrame()
        self.recommendations = []

    # Process the data
    def processData(self):
        # Create a year column and using the year from the title column
        self.movies['year'] = self.movies['title'].str.extract('(\(\d\d\d\d\))', expand=False)
        self.movies['year'] = self.movies['year'].str.extract('(\d\d\d\d)', expand=False)

        # Drop genres from movies
        self.movies.drop(columns=['genre'], inplace=True)

        # Drop movies with no year, get movies in the year 1990s onwards
        self.movies = self.movies[self.movies['year'].notna()]
        self.movies['year'] = self.movies['year'].astype(int)
        self.movies = self.movies.loc[self.movies['year'] >= 1990]

        # Get user history
        self.user_history = self.ratings[self.ratings.userId == self.userId]
        self.user_history.drop(['userId'], axis=1)

    # Get similar users using Pearson correlation
    def getSimilarUsers(self):
        # Get all users who have rated the same movie as the selected user
        similar_users_history = self.ratings[self.ratings['movieId'].isin(self.user_history['movieId'].tolist())]
        similar_users_history = similar_users_history[similar_users_history.userId != self.userId]
        similar_users_history = similar_users_history.groupby(['userId'])

        # Compare user against other users to get the similarity between them
        grouped_similar_users = {}
        for similar_users_id, similar_users_movies in similar_users_history:
            # Drop duplicates
            similar_users_movies = similar_users_movies.drop_duplicates(subset='movieId', keep='first', inplace=False)

            # Sort movie id's of user and similar user's and make it the index
            users_history = self.user_history.sort_values(by='movieId')
            similar_users_history = similar_users_movies.sort_values(by='movieId')
            
            # Get common user ratings relative to similar user
            common_history = users_history[users_history['movieId'].isin(similar_users_history['movieId'])]

            if len(common_history) > 3:
                # Use Pearson correlation to calculate similarity between users
                # Only take at least 2 matching ratings for a similar user
                similarity = pearsonr(common_history.rating.tolist(), similar_users_history.rating.tolist())
                r_value = similarity[0]
                p_value = similarity[1]

                # if r_value is more than or equal to 0.7 and p_value <= 0.05 shows strong correlation
                if r_value >= 0.7 and p_value <= 0.05:
                    grouped_similar_users[similar_users_id] = r_value

        # Create grouped similar users into a Dataframe
        self.similar_users = pd.DataFrame.from_dict(grouped_similar_users, orient='index')

        # Rename column and adjust index
        if len(self.similar_users) > 0:
            self.similar_users.columns = ['similarity']
            self.similar_users['userId'] = self.similar_users.index
            self.similar_users.index = range(len(self.similar_users))

    # Make recommendations to a user
    def recommend(self):
        if len(self.similar_users) > 0:
            # Get the top-10 similar users
            top_similar_users = self.similar_users.sort_values(by='similarity', ascending=False)[:10]

            # Movies and ratings given by top similar users
            similar_ratings = top_similar_users.merge(self.ratings, left_on='userId', right_on='userId', how='inner')
            similar_ratings =  similar_ratings[~similar_ratings['movieId'].isin(self.user_history['movieId'])]
            
            # Create weighted rating (similarity * ratings)
            similar_ratings['weightedRating'] = similar_ratings['similarity'] * similar_ratings['rating']

            # Compile the similarity and ratings of each movie
            compiled_similarity = similar_ratings.groupby('movieId').sum()
            compiled_similarity = compiled_similarity.drop(['userId', 'rating'], axis=1)

            # Create recommendations dataframe and sort based on recommendation score
            recommendations = pd.DataFrame(columns=['recommendation score'])
            recommendations['recommendation score'] = compiled_similarity['weightedRating'] / compiled_similarity[
                'similarity']
            recommendations['movieId'] = compiled_similarity.index
            recommendations = recommendations.sort_values(by='recommendation score', ascending=False)

            # Top 10 movies recommendations
            for movie_id in recommendations['movieId']:
                movie = self.movies.loc[self.movies['movieId'] == movie_id].title.to_string(header=False, index=False)
                if movie != 'Series([], )':
                    self.recommendations.append(movie_id)
                # If there are no 10 recommendations
                if len(self.recommendations) == 10:
                    break


# Content-Based Filtering Recommender
class ContentBasedFiltering(RecommenderBase):
    def __init__(self, uid):
        super().__init__(uid)
        self.similarities = []
        self.user_history = []
        self.recommendations = []

    # Process the data
    def processData(self):
        # Drop genres rows that do not have genres
        self.movies = self.movies[self.movies['genre'] != '(no genres listed)']

        # Get user history
        self.user_history = self.ratings[self.ratings.userId == self.userId]
        self.user_history = self.user_history.drop(['userId', 'rating'], axis=1)
        self.user_history = pd.merge(self.user_history, self.movies, left_on='movieId', right_on='movieId', how='left')

    # Get user and their similarity based on movies that they have rated
    def getSimilarity(self):
        # Tfid Vectorizer which will count the occurrence of genres in a movie
        tf = TfidfVectorizer(analyzer=lambda genres: (i for j in range(1, 4)
                                                           for i in combinations(genres.split(), r=j)))
        tfidf_matrix = tf.fit_transform(self.movies['genre'].tolist())

        # Get the similarity between movies using a cosine similarity metric
        self.similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Recommend similar movies
    def recommend(self):
        total_recommendations = {}
        # Get recommendations for each title
        for selected in self.user_history.iterrows():
            selected_movie_idx = selected[0]
            similar_movies = list(enumerate(self.similarities[selected_movie_idx]))
            sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)

            # Iterate through sorted recommendations for selected movie
            for similar_movie in sorted_similar_movies:
                movie_id = similar_movie[0]
                # If movie is not the selected movie and not in the total recommendations
                if movie_id != selected_movie_idx and movie_id not in total_recommendations:
                    total_recommendations[movie_id] = similar_movie[1]
                elif movie_id != selected_movie_idx and movie_id in total_recommendations:
                    total_recommendations[movie_id] += similar_movie[1]
                else:
                    break

        # Give out top 10 recommendations
        sorted_recommendations = sorted(total_recommendations.items(), key=lambda item: item[1], reverse=True)[:10]
        for movie in sorted_recommendations:
            self.recommendations.append(movie[0])
