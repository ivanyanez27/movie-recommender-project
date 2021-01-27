# Collaborative filtering to get the Top-N recommended movies
import os
import numpy as np
import pandas as pd
from math import sqrt

def main():
    # Read in dataset
    movie_path = os.getcwd() + r'\ml-latest-small\movies.csv'
    ratings_path = os.getcwd() + r'\ml-latest-small\ratings.csv'
    movies = pd.read_csv(movie_path, na_values='NA')
    ratings = pd.read_csv(ratings_path, na_values='NA')

    # Create year column and extract year from the title
    movies['year'] = movies['title'].str.extract('(\(\d\d\d\d\))', expand=False)
    movies['year'] = movies['year'].str.extract('(\d\d\d\d)', expand=False)

    # Drop genres table from movies, timestamp from ratings
    movies.drop(columns=['genres'], inplace=True)
    ratings.drop(columns=['timestamp'], inplace=True)

    # Remove years from movies title
    movies['title'] = [x[:-7] for x in movies['title']]

    # Create a test user profile
    test_user = [
        {'title': 'Breakfast Club, The', 'rating': 4},
        {'title': 'Toy Story', 'rating': 2.5},
        {'title': 'Jumanji', 'rating': 3},
        {'title': 'Pulp Fiction', 'rating': 4.5},
        {'title': 'Akira', 'rating': 5}
    ]

    test_input = pd.DataFrame(test_user)

    # Get the movie id's of movies in test_user
    movie_id = movies[movies['title'].isin(test_input['title'].tolist())]
    test_input = pd.merge(movie_id, test_input)

    # Get all users who have watched the movies in test user profile and group them by users
    users_watched = ratings[ratings['movieId'].isin(test_input['movieId'].tolist())]
    user_group = users_watched.groupby(['userId'])

    # Find the most similar users using Pearson correlation
    similar_users = {}
    for user_id, user_movies in user_group:
        # Sort movie id's of user and test user
        user_movies = user_movies.sort_values(by="movieId")
        test_movies = test_input.sort_values(by="movieId")
        grouped_len = len(test_movies)

        # Get common ratings between test user and user from group
        common_ratings = test_movies[test_movies['movieId'].isin(user_movies['movieId'].tolist())]
        test_ratings = common_ratings['rating'].tolist()
        user_ratings = user_movies['rating'].tolist()

        # Get dictionary matching test user and group user ratings
        test_group_ratings = {}
        for i in range(len(test_ratings)):
            test_group_ratings.update({test_ratings[i]: user_ratings[i]})

        # Use Pearson formula to calculate similarity (x=test user, y=group user)
        xx = sum([i ** 2 for i in test_ratings]) - pow(sum(test_ratings), 2) / float(grouped_len)
        yy = sum([i ** 2 for i in user_ratings]) - pow(sum(user_ratings), 2) / float(grouped_len)
        xy = sum(i * j for i, j in test_group_ratings.items()) - \
             sum(test_ratings) * sum(user_ratings) / float(grouped_len)

        if xx != 0 and yy != 0:
            similar_users[user_id] = xy / sqrt(xx * yy)
        else:
            similar_users[user_id] = 0

    # Create similar_users dict into a Dataframe
    similar_df = pd.DataFrame.from_dict(similar_users, orient='index')

    # Rename column and adjust index
    similar_df.columns = ['similarity']
    similar_df['userId'] = similar_df.index
    similar_df.index = range(len(similar_df))

    # Find the top-10 similar users
    top_similar_users = similar_df.sort_values(by='similarity', ascending=False)[:10]
    print(top_similar_users)


main()
