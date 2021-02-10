import os
import pandas as pd
from scipy.stats import pearsonr


class CollaborativeFiltering:

    def __init__(self):
        self.movies = []
        self.user_id = 00
        self.ratings = []
        self.user_history = []
        self.similar_df = pd.DataFrame()

    # Preprocess the dataset
    def preprocess(self):
        # Load in dataset
        movie_path = os.getcwd() + r'\ml-latest-small\movies.csv'
        ratings_path = os.getcwd() + r'\ml-latest-small\ratings.csv'
        movies = pd.read_csv(movie_path, na_values='NA')
        ratings = pd.read_csv(ratings_path, na_values='NA')

        # Create a year column and using the year from the title column
        movies['year'] = movies['title'].str.extract('(\(\d\d\d\d\))', expand=False)
        movies['year'] = movies['year'].str.extract('(\d\d\d\d)', expand=False)

        # Drop genres from movies, and timestamp from ratings
        movies.drop(columns=['genres'], inplace=True)
        ratings.drop(columns=['timestamp'], inplace=True)

        # Remove the years from movies title column
        movies['title'] = [x[:-7] for x in movies['title']]

        # Set movies and ratings
        self.movies = movies
        self.ratings = ratings

    # Get recommenders user ID
    def getUserId(self):
        user_previous_ratings = [
            {'title': 'Iron Man 2', 'rating': 4},
            {'title': 'Toy Story', 'rating': 2.5},
            {'title': 'Avengers: Age of Ultron', 'rating': 3},
            {'title': 'Iron Man 3', 'rating': 4.5},
            {'title': 'Captain America: Civil War', 'rating': 5}
        ]

        self.user_history = pd.DataFrame(user_previous_ratings)

    # Get similar users using Pearson correlation
    def getSimilarUsers(self):
        # Get the movie id's of the user being recommended and create a user movie dataframe
        movie_ids = self.movies[self.movies['title'].isin(self.user_history['title'].tolist())]
        self.user_history = pd.merge(movie_ids, self.user_history)

        # Get all users who share the same movie ratings history and group them
        similar_users = self.ratings[self.ratings['movieId'].isin(self.user_history['movieId'].tolist())]
        similar_users = similar_users.groupby(['userId'])

        # Compare user against other users to get the similarity between them
        grouped_similar_users = {}
        for similar_user_id, similar_user_movies in similar_users:
            # Sort movie id's of user and similar users
            similar_user_movies = similar_user_movies.sort_values(by='movieId')
            user_movies = self.user_history.sort_values(by='movieId')

            # Get common ratings between user and similar user
            common_ratings = user_movies[user_movies['movieId'].isin(similar_user_movies['movieId'].tolist())]
            similar_user_ratings = similar_user_movies['rating'].tolist()
            user_ratings = common_ratings['rating'].tolist()

            # Contain matching ratings in a dictionary
            matching_ratings = {}
            for i in range(len(similar_user_ratings)):
                matching_ratings.update({similar_user_ratings[i]: user_ratings[i]})

            # Use Pearson correlation to calculate similarity between users
            # Only take at least 2 matching ratings for a similar user
            if len(matching_ratings) >= 2:
                similarity = pearsonr(similar_user_ratings, user_ratings)
                r_value = similarity[0]
                p_value = similarity[1]

                # if r_value is more than 0.7 and p value <= 0.05 shows strong correlation
                if r_value >= 0.7:
                    grouped_similar_users[similar_user_id] = r_value

        # Create grouped similar users into a Dataframe
        self.similar_df = pd.DataFrame.from_dict(grouped_similar_users, orient='index')

        # Rename column and adjust index
        self.similar_df.columns = ['similarity']
        self.similar_df['userId'] = self.similar_df.index
        self.similar_df.index = range(len(self.similar_df))

    # Make recommendations to a user
    def make_recommendations(self):
        # Get the top-10 similar users
        top_similar_users = self.similar_df.sort_values(by='similarity', ascending=False)[:10]

        # Movies and ratings given by top similar users
        top_similar_ratings = top_similar_users.merge(self.ratings, left_on='userId', right_on='userId', how='inner')

        # Create weighted rating (similarity * ratings)
        top_similar_ratings['weightedRating'] = top_similar_ratings['similarity'] * top_similar_ratings['rating']

        # Compile the similarity and ratings of each movie
        compiled_similarity_ratings = top_similar_ratings.groupby('movieId').sum()
        compiled_similarity_ratings = compiled_similarity_ratings.drop(['userId', 'rating'], axis=1)

        # Create recommendations dataframe and sort based on recommendation score
        recommendations = pd.DataFrame(columns=['recommendation score'])
        recommendations['recommendation score'] = compiled_similarity_ratings['weightedRating'] / \
                                                  compiled_similarity_ratings['similarity']
        recommendations['movieId'] = compiled_similarity_ratings.index
        recommendations = recommendations.sort_values(by='recommendation score', ascending=False)[:10]

        # Top 10 movies recommendations
        for movie_id in recommendations.index:
            print(self.movies.loc[self.movies['movieId'] == movie_id].title)


a = CollaborativeFiltering()
a.preprocess()
a.getUserId()
a.getSimilarUsers()
a.make_recommendations()