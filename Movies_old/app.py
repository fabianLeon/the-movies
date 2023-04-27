from flask import Flask
import numpy as np
import pandas as pd
movies_df = pd.read_csv("movies_all_data.csv")
similarity_matrix = np.loadtxt("similarity_matrix.csv", delimiter=",")

app = Flask(__name__)

@app.route('/movies')
def movies(movie):
    id_of_movie = movies_df[movies_df['title']==movie].index[0]
    distances = similarity_matrix[id_of_movie]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:15]

    contador = 0
    for movie_id in similarity_matrix:
        print(movie_id)
        contador += 1
        if(contador > 5):
            break

    for movie_id in movie_list:
        print(movies_df.iloc[movie_id[0]].title)
    return 'Hello, World!'