from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
import pandas as pd
from tokenGenerator import tokenApi
similarity_matrix = np.loadtxt("similarity_matrix.csv", delimiter=",")

user = {"a": [similarity_matrix, similarity_matrix, similarity_matrix],
        "b": [similarity_matrix, similarity_matrix, similarity_matrix],
        "c": [similarity_matrix, similarity_matrix, similarity_matrix]}


movies_df = pd.read_csv("movies_all_data.csv")

app = Flask(__name__)
CORS(app)


@app.route('/<token>')
def hello_world(token):
    ini = 1
    end = 5
    movie_data = []

    if 'token' in request.view_args and len(user[token]) > 0:
        for item in user[token]:
            id_of_movie = movies_df[movies_df['title']=='Toy Story'].index[0]
            distances = similarity_matrix[id_of_movie]
            movie_list = sorted(list(enumerate(distances)),
                                reverse=True, key=lambda x: x[1])[1:5]
            # ini += 1
            # end += end
            # distances2lvl = item
            # movie_list.append = sorted(list(enumerate(distances2lvl)),
            #                            reverse=True, key=lambda x: x[6])[6:10]
            # distances3lvl = item
            # movie_list.append = sorted(list(enumerate(distances3lvl)),
            #                            reverse=True, key=lambda x: x[10])[10:5]
    else:
        distances = similarity_matrix[862]
        movie_list = sorted(list(enumerate(distances)),
                            reverse=True, key=lambda x: x[1])[1:15]

    for movie_id in movie_list:
        data = movies_df.iloc[movie_id[0]]
        movie_data.append(
            {"id": int(data["id"]), "title": data["title"], "tags": data["tags"]})

    return jsonify(movie_data)


@app.route('/tkn', methods=["POST"])
def generator():
    code = tokenApi(request.json)
    result = {"token": code}
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
