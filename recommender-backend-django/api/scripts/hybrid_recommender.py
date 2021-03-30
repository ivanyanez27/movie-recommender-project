import pandas as pd
from scipy.stats import pearsonr
from itertools import combinations
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


# Base for recommenders
class RecommenderBase:
    def __init__(self, uid):
        self.userId = uid
        self.movies = None
        self.ratings = None

    def queryset_to_df(self):
        movie_id_list = [obj.id for obj in self.movies.objects.all()]
        title_list = [obj.title for obj in self.movies.objects.all()]
        genre_list = [obj.genre for obj in self.movies.objects.all()]

        self.movies = pd.DataFrame({
            'movieId': movie_id_list,
            'title': title_list,
            'genre': genre_list
        })

        user_id_list = [obj.user.id for obj in self.ratings.objects.all()]
        movie_id_list = [obj.movie.id for obj in self.ratings.objects.all()]
        rating_list = [float(obj.rating) for obj in self.ratings.objects.all()]

        self.ratings = pd.DataFrame({
            'userId': user_id_list,
            'movieId': movie_id_list,
            'rating': rating_list
        })


# Collaborative Filtering Recommender
class CollaborativeFiltering(RecommenderBase):
    def __init__(self, uid):
        super().__init__(uid)
        self.user_history = []
        self.similar_df = pd.DataFrame()

    # Process the data
    def processData(self):
        # Create a year column and using the year from the title column
        self.movies['year'] = self.movies['title'].str.extract('(\(\d\d\d\d\))', expand=False)
        self.movies['year'] = self.movies['year'].str.extract('(\d\d\d\d)', expand=False)
        self.movies.drop(columns=['genre'], inplace=True)

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

        # Create weighted similarity rating (similarity * ratings)
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
        print("---------------------------------------------------------------------")


# Content-Based Filtering Recommender
class ContentBasedFiltering(RecommenderBase):
    def __init__(self, uid):
        super().__init__(uid)
        self.similarities = []
        self.user_history = []

    # Process data
    def processData(self):
        self.movies = self.movies[self.movies['genre'].str.contains("(no genres listed)")]

    # Get user and their previous movies
    def getSimilarity(self):
        self.user_history = self.ratings[self.ratings.userId == self.userId]
        self.user_history = self.user_history.drop(['userId', 'rating'], axis=1)
        self.user_history = pd.merge(self.user_history, self.movies, left_on='movieId', right_on='movieId', how='left')

        # Tfid Vectorizer which will count the occurrence of genres in a movie
        tf = TfidfVectorizer(analyzer=lambda s: (x for y in range(1, 4)
                                                 for x in combinations(s.split('|'), r=y)))
        tfidf_matrix = tf.fit_transform(self.user_history['genre'])

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
                movie_title = self.movies[self.movies.index == similar_movie[0]].title.values[0]
                # If movie is not the selected movie and not in the total recommendations
                if similar_movie[0] != selected_movie_idx and movie_title not in total_recommendations:
                    total_recommendations[movie_title] = similar_movie[1]
                elif similar_movie[0] != selected_movie_idx and movie_title in total_recommendations:
                    total_recommendations[movie_title] += similar_movie[1]
                else:
                    break

        # Give out top 10 recommendations
        sorted_recommendations = sorted(total_recommendations.items(), key=lambda item: item[1], reverse=True)[:10]
        # common_ratings = user_movies[user_movies['movieId'].isin(similar_user_movies['movieId'].tolist())]
        print("---------------------------------------------------------------------")
        print("Recommended movies based on previous interaction of movies:")
        for movie in sorted_recommendations:
            print(movie[0])
        print("---------------------------------------------------------------------")


class HybridRecommender:
    def __init__(self, collabFilter, contentFilter):
        super.__init__()
        self.collabFilter = collabFilter
        self.contentFilter = contentFilter
        self.recommendation = {}

    # Run collab filter processes
    def runCollaborativeFiltering(self):
        self.collabFilter.processData()
        self.collabFilter.getUserHistory()
        self.collabFilter.getSimilarUsers()
        self.collabFilter.recommend()

    # Run content filter processes
    def runContentFiltering(self):
        self.contentFilter.getSimilarity()

    # Get recommendations
    def getResults(self):
        cbfResult = self.collabFilter.recommend()
        cnfResult = self.contentFilter.recommend()

        if 'recommendation' in self.recommendation:
            updated = {'recommendation': cbfResult + cnfResult}
            self.recommendation.update(updated)
        else:
            self.recommendation = {'recommendation': cbfResult + cnfResult}


def run():
    uid = 2

    cbf = CollaborativeFiltering(uid=uid)
    cbf.processData()



    print('test')
    """Works 
    cbf = CollaborativeFiltering(uid)
    cbf.processData()
    cbf.getUserHistory()
    cbf.getSimilarUsers()
    cbf.recommend()
    
    # Setup content based filtering
    cnf = ContentBasedFiltering(uid)
    cnf.processData()
    #cnf.getSimilarity()

    # Setup hybrid recommender
    hybrid = HybridRecommender(cbf, cnf)
    hybrid.processDatasets()
    hybrid.runCollaborativeFiltering()
    hybrid.runContentFiltering()
    hybrid.getResults()

    # Return recommendations
    print(hybrid.recommendation)
    # recommend_list = {'recommend': hybrid.recommend()}
    # return recommend_list 
    print(cnf.userId)"""
