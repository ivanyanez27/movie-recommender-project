import os
import math
import numpy as np
import pandas as pd
from itertools import combinations
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


# Recommend top 15 similar movies
def movie_recommendations(similar_movies, movie_set, test_movie):
    recommended = []
    for movie in similar_movies:
        if len(recommended) != 15:
            movie_title = getMovieTitle(movie[0], movie_set, test_movie)

            # If the movie is not the test movie
            if movie_title != test_movie:
                recommended.append(movie_title)

        else:
            break

    for recommendation in recommended:
        print(recommendation)

# Include tags in the content based
# def combined_features(row):
# return row['keywords'] + " " + row['cast'] + " " + row['genres'] + " " + row['director']


def getMovieIdx(title, movies):
    a = movies[movies.title == title].index
    b = a.values[0]
    return b


def getMovieTitle(index, movies, test_movie='N/A'):
    movie = movies[movies.index == index].title.values[0]
    return movie


def main():
    # Read in dataset
    movie_path = os.getcwd() + r'\ml-latest-small\movies.csv'
    ratings_path = os.getcwd() + r'\ml-latest-small\ratings.csv'

    movies = pd.read_csv(movie_path, na_values='NaN')
    ratings = pd.read_csv(ratings_path, na_values='NaN')

    # Remove years from movies title
    movies['title'] = [x[:-7] for x in movies['title']]

    # Drop timestamp column and add index as a column
    movies.dropna(subset=['genres'], inplace=True)
    movies_ratings = pd.merge(ratings, movies, on='movieId')
    movies_ratings.drop(columns=['timestamp'], inplace=True)
    movies_ratings.dropna(subset=['genres'], inplace=True)

    # Tfid Vectorizer which will count the occurrence of genres in a movie
    tf = TfidfVectorizer(analyzer=lambda s: (x for y in range(1, 4)
                                             for x in combinations(s.split('|'), r=y)))
    tfidf_matrix = tf.fit_transform(movies['genres'])

    # Get the similarity between movies using a cosine similarity metric
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Test the recommendation
    test_movie = "Iron Man 3"
    movie_index = getMovieIdx(test_movie, movies)
    similar_movies = list(enumerate(cosine_sim[movie_index]))
    sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)

    # Show the recommended movie
    movie_recommendations(sorted_similar_movies, movies, test_movie)

main()