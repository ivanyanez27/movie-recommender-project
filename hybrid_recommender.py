import os
import pandas as pd
from scipy.stats import pearsonr
from itertools import combinations
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


# Base for recommenders
class RecommenderBase:
    def __init__(self):
        self.movies = []
        self.ratings = []
        self.userId = 1
        self.getData()

    # Get movie data
    def getData(self):
        movie_path = os.getcwd() + r'\ml-latest-small\movies.csv'
        ratings_path = os.getcwd() + r'\ml-latest-small\ratings.csv'
        # movie_path = os.getcwd() + r'\dataset\movies.csv'
        # ratings_path = os.getcwd() + r'\dataset\ratings.csv'
        self.movies = pd.read_csv(movie_path, na_values='NaN')
        self.ratings = pd.read_csv(ratings_path, na_values='NaN')


# Collaborative Filtering Recommender
class CollaborativeFiltering(RecommenderBase):
    def __init__(self):
        super().__init__()
        self.user_history = []
        self.similar_df = pd.DataFrame()

    # Process the data
    def processData(self):
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

    # Get user and their previous ratings history
    def getUserHistory(self):
        self.user_history = self.ratings[self.ratings.userId == self.userId]
        self.user_history.drop(['userId'], axis=1)

    # Get similar users using Pearson correlation
    def getSimilarUsers(self):
        # Get all users who share the same movie ratings history and group them
        similar_users = self.ratings[self.ratings['movieId'].isin(self.user_history['movieId'].tolist())]
        similar_users = similar_users[similar_users.userId != self.userId]
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
    def recommend(self):
        # Get the top-10 similar users
        similar_users = self.similar_df.sort_values(by='similarity', ascending=False)[:10]

        # Movies and ratings given by top similar users
        similar_ratings = similar_users.merge(self.ratings, left_on='userId', right_on='userId', how='inner')

        # Create weighted rating (similarity * ratings)
        similar_ratings['weightedRating'] = similar_ratings['similarity'] * similar_ratings['rating']

        # Compile the similarity and ratings of each movie
        compiled_similarity = similar_ratings.groupby('movieId').sum()
        compiled_similarity = compiled_similarity.drop(['userId', 'rating'], axis=1)

        # Create recommendations dataframe and sort based on recommendation score
        recommendations = pd.DataFrame(columns=['recommendation score'])
        recommendations['score'] = compiled_similarity['weightedRating'] / compiled_similarity['similarity']
        recommendations['movieId'] = compiled_similarity.index
        recommendations = recommendations.sort_values(by='score', ascending=False)[:10]

        # Top 10 movies recommendations
        print("---------------------------------------------------------------------")
        print("Recommended movies based on user's ratings with similar users:")
        for movie_id in recommendations['movieId']:
            print(self.movies.loc[self.movies['movieId'] == movie_id].title.to_string(header=False, index=False))


# Content-Based Filtering Recommender
class ContentBasedFiltering(RecommenderBase):
    def __init__(self):
        super().__init__()
        self.movies_ratings = []
        self.similarities = []
        self.user_history = []
        self.processData()

    # Process the data
    def processData(self):
        movie_path = os.getcwd() + r'\ml-latest-small\movies.csv'
        ratings_path = os.getcwd() + r'\ml-latest-small\ratings.csv'

        self.movies = pd.read_csv(movie_path, na_values='NaN')
        self.ratings = pd.read_csv(ratings_path, na_values='NaN')

        # Remove years from movies title
        self.movies['title'] = [x[:-7] for x in self.movies['title']]

        # Drop timestamp column and add index as a column
        self.movies.dropna(subset=['genres'], inplace=True)
        self.movies_ratings = pd.merge(self.ratings, self.movies, on='movieId')
        self.movies_ratings.drop(columns=['timestamp'], inplace=True)
        self.movies_ratings.dropna(subset=['genres'], inplace=True)

    # Get movie id
    def getMovieId(self, selected_title):
        movie_details = self.movies[self.movies.title == selected_title].index
        movie_id = movie_details.values[0]
        return movie_id

    # Get movie titles
    def getMovieTitle(self, index):
        movie = self.movies[self.movies.index == index].title.values[0]
        return movie

    # Get user and their previous ratings history
    def getUserHistory(self):
        self.user_history = self.ratings[self.ratings.userId == self.userId]
        self.user_history = self.user_history.drop(['userId', 'rating', 'timestamp'], axis=1)
        movies_history = self.movies[self.movies['movieId'].isin(self.user_history['movieId'].tolist())]
        self.getSimilarity(movies_history)

    # Train the model
    def getSimilarity(self, movies_history):
        # Tfid Vectorizer which will count the occurrence of genres in a movie
        tf = TfidfVectorizer(analyzer=lambda s: (x for y in range(1, 4)
                                                 for x in combinations(s.split('|'), r=y)))
        tfidf_matrix = tf.fit_transform(self.movies_history['genres'])

        # Get the similarity between movies using a cosine similarity metric
        self.similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Recommend top n similar movies
    def recommend(self):
        total_recommendations = {}
        # Get recommendations for each title
        for selected in self.user_history.iterrows():
            movie_idx = int(selected[1].to_string(header=False, index=False))
            similar_movies = list(enumerate(self.similarities[movie_idx]))
            sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)

            # Iterate through sorted recommendations for selected movie
            for movie in sorted_similar_movies:
                movie_title = self.getMovieTitle(movie[0])
                # If movie is not the selected movie and not in the total recommendations
                if movie[0] != movie_idx and movie_title not in total_recommendations:
                    total_recommendations[movie_title] = movie[1]
                elif movie[0] != movie_idx and movie_title in total_recommendations:
                    total_recommendations[movie_title] += movie[1]
                else:
                    break

        # Sort through the overall recommendations
        sorted_recommendations = sorted(total_recommendations, key=lambda x: x[1], reverse=True)

        # Give out top 10 recommendations
        print("---------------------------------------------------------------------")
        print("Recommended movies based on previous interaction movies with similar users:")
        for i in range(10):
            print(sorted_recommendations[i])


class HybridRecommender:
    def __init__(self, collabFilter, contentFilter):
        self.collabFilter = collabFilter()
        self.contentFilter = contentFilter()
        self.cachedResults = {}

    # Run collab filter processes
    def runCollaborativeFiltering(self):
        self.collabFilter.processData()
        self.collabFilter.getUserHistory()
        self.collabFilter.getSimilarUsers()

    # Run content filter processes
    def runContentFiltering(self):
        self.contentFilter.processData()
        self.contentFilter.getUserHistory()
        self.contentFilter.recommend()

    # Get recommendations
    def getResults(self):
        cbfResult = self.collabFilter.recommend()
        cnfResult = self.contentFilter.recommend()

    def makeRecommendations(self):
        pass


base = RecommenderBase()
cbf = CollaborativeFiltering
cnf = ContentBasedFiltering
hybrid = HybridRecommender(cbf, cnf)
hybrid.runContentFiltering()
print('')
