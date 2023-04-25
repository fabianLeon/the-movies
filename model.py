# Steep one, implement imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from tqdm import tqdm
import warnings
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer

plt.style.use("fivethirtyeight")
warnings.filterwarnings("ignore")

# loading datasets

movies_md = pd.read_csv("movies_metadata.csv")
movies_keywords = pd.read_csv("keywords.csv")
movies_credits = pd.read_csv("credits.csv")


movies_md.head()
movies_md.info()
movies_keywords.head()

movies_md = movies_md[movies_md['vote_count'] >= 55]

movies_md.head()
movies_md.columns

movies_md = movies_md[['id', 'original_title', 'overview', 'genres']]

movies_md.head()

movies_md['title'] = movies_md['original_title']

movies_md.head()


movies_md.reset_index(inplace=True, drop=True)

movies_md.head()

movies_credits = movies_credits[['id', 'cast']]

movies_credits.head()

len(movies_md)

movies_md = movies_md[movies_md['id'].str.isnumeric()]

len(movies_md)

movies_md['id'] = movies_md['id'].astype(int)

movies_df = pd.merge(movies_md, movies_keywords, on='id', how='left')

movies_df.head()

movies_df.reset_index(inplace=True, drop=True)

movies_df = pd.merge(movies_df, movies_credits, on='id', how='left')
movies_df.reset_index(inplace=True, drop=True)

movies_df.head()

movies_df['genre'] = movies_df['genres'].apply(
    lambda x: [i['name'] for i in eval(x)])

movies_df.head()

movies_df['genre'] = movies_df['genre'].apply(
    lambda x: [i.replace(" ", "") for i in x])

movies_df.head()

movies_df.isnull().sum()

movies_df['keywords'].fillna('[]', inplace=True)
movies_df['genre'] = movies_df['genre'].apply(lambda x: ' '.join(x))

movies_df.head()

movies_df.drop('genres', axis=1, inplace=True)
movies_df.head()

movies_df['cast'] = movies_df['cast'].apply(
    lambda x: [i['name'] for i in eval(x)])
movies_df['cast'] = movies_df['cast'].apply(
    lambda x: ' '.join([i.replace(" ", "") for i in x]))

movies_df['keywords'] = movies_df['keywords'].apply(
    lambda x: [i['name'] for i in eval(x)])
movies_df['keywords'] = movies_df['keywords'].apply(
    lambda x: ' '.join([i.replace(" ", "") for i in x]))

movies_df.head()
movies_df['tags'] = movies_df['overview']+' '+movies_df['keywords']+' ' + \
    movies_df['cast']+' '+movies_df['genre']+' '+movies_df['original_title']
movies_df['tags']

movies_df.drop(['genre', 'original_title', 'keywords',
               'cast', 'overview'], axis=1, inplace=True)

movies_df.head()
movies_df.isnull().sum()

movies_df.drop(movies_df[movies_df['tags'].isnull()].index, inplace=True)

movies_df.shape
movies_df.drop_duplicates(inplace=True)
movies_df.shape

movies_df.to_csv("movies_all_data.csv", index=False)


# Common words have less IDF
# Unique Words have high IDF
tfidf = TfidfVectorizer(max_features=5000)

vectorized_data = tfidf.fit_transform(movies_df['tags'].values)

tfidf.get_feature_names_out()

vectorized_dataframe = pd.DataFrame(
    vectorized_data.toarray(), index=movies_df['tags'].index.tolist())

vectorized_dataframe.head()

vectorized_dataframe.shape


svd = TruncatedSVD(n_components=3000)

reduced_data = svd.fit_transform(vectorized_dataframe)

reduced_data.shape

reduced_data

svd.explained_variance_ratio_.cumsum()


similarity = cosine_similarity(reduced_data)

np.savetxt("similarity_matrix.csv", similarity, delimiter=",")

# import pickle

# with open('similarity_model.pkl', 'wb') as f:
#     pickle.dump(similarity, f)
