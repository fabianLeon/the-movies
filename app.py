from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import json
import pandas as pd
movies_df = pd.read_csv("movies_all_data.csv")
similarity_matrix = np.loadtxt("similarity_matrix.csv", delimiter=",")
movies_metadata = pd.read_csv("movies_merge_metadata.csv")

len(movies_metadata)
movies_metadata.info()



app = Flask(__name__)
cors = CORS(app, resources={r"/movies": {"origins": "http://localhost"}})

@app.route('/movies', methods=['POST'])
def movies():
    movies_json = request.get_json()
    movie = movies_json['movie']

    id_of_movie = movies_df[movies_df['title']==movie].index[0]
    print(id_of_movie)
    distances = similarity_matrix[id_of_movie]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:15]
    movie_metadata = movies_metadata.reset_index(drop=True)

    movies_list = []
    for movie_id in movie_list:
        try:
            movie_id = movies_df.iloc[movie_id[0]].id
            print(type(movie_id))
            print(movie_id)
            movie_metadata = movies_metadata[movies_metadata.id == movie_id]
            jsondata = movie_metadata.to_json()
            movies_list.append(json.loads(jsondata))
        except TypeError:
            print('ups')
        # Realizamos alguna operación con los datos recibidos (en este ejemplo, simplemente los devolvemos en un nuevo JSON)
    response_json = {'received_movies': movies_list}

    # Enviamos la respuesta en formato JSON
    return jsonify(response_json)

@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost" # <- You can change "*" for a domain for example "http://localhost"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
    return response



