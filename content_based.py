import os
import pandas as pd
from itertools import combinations
from sklearn.feature_extraction.text import TfidfVectorizer



def main():
    # Read in dataset
    movie_path = os.getcwd() + r'\ml-latest-small\movies.csv'
    ratings_path = os.getcwd() + r'\ml-latest-small\ratings.csv'
    tags_path = os.getcwd() + r'\ml-latest-small\tags.csv'

    movies = pd.read_csv(movie_path, na_values='NA')[:5]
    ratings = pd.read_csv(ratings_path, na_values='NA')[:5]
    tags = pd.read_csv(tags_path, na_values='NA')[:5]

    # Drop timestamp column
    tags.drop(columns=['timestamp'], inplace=True)

    # Create item feature vector using TFID
    vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
    vectorizer.fit(tags['tag'])
    #print(vectorizer.get_feature_names())

    test_vect = [x for i in range(1, 4) for x in combinations(tags['tag'], r=i)]

    print(test_vect)
    
main()