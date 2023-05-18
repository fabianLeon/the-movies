from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def processVector(vector=None):
    if vector is None:
        return 0
    else:
        # returnnp.sum(vector.data)
        # return np.prod(vector.data)
        # return np.linalg.norm(vector.data)
        return np.linalg.norm(vector.data, ord=1)


movies_md = pd.read_csv("movies_all_data_nosplit.csv")
movies_md = movies_md.fillna("")
tfidf_vectors = np.zeros(
    shape=(len(movies_md), len(movies_md.columns)), dtype=object)
for indice, fila in movies_md.iterrows():
    columna_vectors = []
    for valor in fila.values:
        if not valor.strip():
            columna_vectors.append(processVector())
            continue
        vector = TfidfVectorizer(
            min_df=1,
            stop_words=None,
            token_pattern=r"(?u)\b\w+\b|[\u4e00-\u9fff]+|[A-Za-z\.&]+\S*",
        ).fit_transform([str(valor)])
        columna_vectors.append(processVector(vector))
    tfidf_vectors[indice] = columna_vectors
tfidf_vectors = pd.DataFrame(tfidf_vectors, columns=movies_md.columns)

(
    datos_entrenamiento,
    datos_pruebas,
    objetivo_entrenamiento,
    objetivo_pruebas,
) = train_test_split(
    tfidf_vectors.iloc[:, :-1],
    tfidf_vectors.iloc[:, -1],
)

arbol = tree.ExtraTreeRegressor(max_depth=10)
modelo = arbol.fit(datos_entrenamiento, objetivo_entrenamiento)
score_entrenamiento = arbol.score(
    datos_entrenamiento, objetivo_entrenamiento
)
score_pruebas = arbol.score(datos_pruebas, objetivo_pruebas)

print(tree.export_text(modelo,
                       feature_names=["overview",	"keywords", "cast", "genre"]))
print(score_entrenamiento)
print(score_pruebas)
plt.figure(figsize=(12, 6))
tree.plot_tree(modelo, feature_names=["overview",	"keywords", "cast", "genre"])
plt.show()
