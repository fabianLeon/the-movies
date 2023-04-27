from flask import Flask, jsonify, request
import flask_cors as CORS
import numpy as np
import pandas as pd
import json
from query import get_similitary
from tokenGenerator import tokenApi
similarity_matrix = np.loadtxt("Movies_old/similarity_matrix.csv", delimiter=",")

user = {}


tags = pd.read_csv("keywords.csv")
movies_df = pd.read_csv("movies_all_data.csv")

app = Flask(__name__)
CORS(app)


@app.route('/<token>')
def hello_world(token):
    movie_data = []
    if 'token' in request.view_args:
        if token not in user.keys():
            user[token] = []
        tagsMovie = json.loads(
            tags[tags['id'] == 862]["keywords"]._values[0].replace("'", "\"")
            #tags[tags['id'] == 9571]["keywords"]._values[0].replace("'", "\"")
            )
        for item in tagsMovie:
            objChk = {"count": 0, "tag": item['name']}
            if len(user[token]) > 0:
                index = next((i for i, obj in enumerate(
                    user[token]) if item['name'] == obj['tag']), None)

                if index is not None:
                    user[token][index]["count"] += 1
                else:
                    user[token].append(objChk)
            else:
                user[token].append(objChk)

        sorted_objects = sorted(user[token], key=lambda obj: obj['count'])
        string_result = " ".join(str(obj['tag']) for obj in sorted_objects)

        movie_list = get_similitary(string_result)
    else:
        movie_list = sorted(list(enumerate(movies_df)),
                            reverse=True, key=lambda x: x[1])[1:15]

    for data in movie_list:
        movie_data.append(
            {"id": int(data["idMovie"]), "title": data["title"]})

    return jsonify(movie_data)


@app.route('/tkn', methods=["POST"])
def generator():
    code = tokenApi(request.json)
    result = {"token": code}
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
