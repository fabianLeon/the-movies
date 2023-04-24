from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
movies_df = pd.read_csv("movies_all_data.csv")
similarity_matrix = np.loadtxt("similarity_matrix.csv", delimiter=",")

app = Flask(__name__)

@app.route('/movies', methods=['POST'])
def movies():
    movies_json = request.get_json()
    movie = movies_json['movie']
    print(movie)

    id_of_movie = movies_df[movies_df['title']==movie].index[0]
    distances = similarity_matrix[id_of_movie]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:15]

    contador = 0
    for movie_id in similarity_matrix:
        print(movie_id)
        contador += 1
        if(contador > 5):
            break
    
    contador = 0
    for movie_id in movies_df:
        print(movie_id)
        contador += 1
        if(contador > 5):
            break

    movies_list = []
    for movie_id in movie_list:
        movies_list.append(movies_df.iloc[movie_id[0]].title)
        print(movies_df.iloc[movie_id[0]].title)


    # Realizamos alguna operación con los datos recibidos (en este ejemplo, simplemente los devolvemos en un nuevo JSON)
    response_json = {'received_movies': movies_list}

    # Enviamos la respuesta en formato JSON
    return jsonify(response_json)