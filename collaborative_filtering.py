# Collaborative filtering

import pandas as pd
from surprise import SVD, Reader, Dataset
from surprise.model_selection import cross_validate

# features
movie_features = ['movieId', 'title', 'genre']
ratings_features = ['userId', 'movieId', 'rating', 'timestamp']

# Read in dataset
movies = pd.read_csv(r'C:\Users\Ivan Yanez\movie-recommender-system\ml-latest-small\movies.csv', names=movie_features)
ratings = pd.read_csv(r'C:\Users\Ivan Yanez\movie-recommender-system\ml-latest-small\ratings.csv',
                      names=ratings_features)

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