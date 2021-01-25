# Collaborative filtering to get the Top-N recommended movies
import os
import numpy as np
import pandas as pd


def main():
    # Read in dataset
    movie_path = os.getcwd() + r'\ml-latest-small\movies.csv'
    ratings_path = os.getcwd() + r'\ml-latest-small\ratings.csv'
    movies = pd.read_csv(movie_path, na_values='NA')
    ratings = pd.read_csv(ratings_path, na_values='NA')

    # Create year column from the title
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
    users_subset = users_watched.groupby(['userId'])
    print(users_subset.get_group(4))

    # Find the most similar users using Pearson correlation

main()