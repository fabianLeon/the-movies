from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
import pandas as pd
import json
from tokenGenerator import tokenApi
similarity_matrix = np.loadtxt("similarity_matrix.csv", delimiter=",")

user = {"a": [],
        "b": [],
        "c": []}


tags = pd.read_csv("keywords.csv" )
movies_df = pd.read_csv("movies_all_data.csv")

app = Flask(__name__)
CORS(app)


@app.route('/<token>')
def hello_world(token):
    ini = 1
    end = 5 
    movie_data = [] 
    if 'token' in request.view_args  :
        tagsMovie =json.loads(tags[tags['id'] == 862]["keywords"][0].replace("'", "\""))  
        for item in tagsMovie :
            if  len(user[token])>0:
                for savetags in user[token]:
                    if  item['name']  == savetags["tag"]:   
                        savetags["count"]+=1 
                        break 
            else:
                user[token].append({"count":0,"tag":item['name']}) 
        
        distances = similarity_matrix[862]
        movie_list = sorted(list(enumerate(distances)),
                reverse=True, key=lambda x: x[1])[1:5]
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
