# Collaborative filtering
import os
import numpy as np
import pandas as pd
from surprise import SVD, Reader, Dataset
from surprise.model_selection import cross_validate


# Get unique genres across all movies
def getUniqueGenres(genres):
    unique_genres = []
    for row in genres:
        # if there are multiple genres
        if '|' in row:
            genre_list = row.split('|')
            # Add genre if not in genre list
            for genre in genre_list:
                if genre not in unique_genres:
                    unique_genres.append(genre)

    unique_genres = sorted(unique_genres)
    return unique_genres


def main():
    # Read in dataset
    movie_path = os.getcwd() + r'\ml-latest-small\movies.csv'
    ratings_path = os.getcwd() + r'\ml-latest-small\ratings.csv'
    movie_data = pd.read_csv(movie_path, na_values='NA')
    ratings = pd.read_csv(ratings_path, na_values='NA')

    # get unique users, movies and genres
    users = ratings.userId.unique()
    movies = movie_data.movieId.unique()
    genres = getUniqueGenres(movie_data['genres'])

    # get the top 20 users who have rated frequently
    top_users = ratings.groupby('userId')['rating'].count()
    sorted_top_users = top_users.sort_values(ascending=False)[0:15]

    # get the top 20 movies that have been rated frequently
    top_movies = ratings.groupby('movieId')['rating'].count()
    sorted_top_movies = top_movies.sort_values(ascending=False)[0:15]

    # create user-movie matrix
    um_matrix = ratings.join(sorted_top_users, on='userId', how='inner', rsuffix='_r')
    um_matrix = um_matrix.join(sorted_top_movies, on='userId', how='inner', rsuffix='_r')
    a = pd.crosstab(um_matrix.userId, um_matrix.movieId, um_matrix.rating, aggfunc=np.sum)



main()

'''
ratings_dict = {'movieId': list(ratings.movieId),
                'userId': list(ratings.userId),
                'rating': list(ratings.rating)}

df = pd.DataFrame(ratings_dict)

# parse through rating files
reader = Reader(rating_scale=(0.5, 5.0))

######################
# TEST SVD ALGORITHM #
######################

# load a dataset
data = Dataset.load_builtin('ml-100k')

# use SVD algorithm
algorithm = SVD()

# run a 5 cross-validation fold
cross_validate(algorithm, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)
'''
