import weaviate
client = weaviate.Client(url="https://moviexpredeitor-77pe0djc.weaviate.network")
#client.schema.delete_all() #Si se desea eliminar todos los schemas

class_obj = {
    "class": "Movie",
    "vectorizer": "none",  # Or "text2vec-cohere" or "text2vec-huggingface"
}
client.schema.create_class(class_obj)


class_obj = {
    "class": "cdt",
    "vectorizer": "none",  # Or "text2vec-cohere" or "text2vec-huggingface"
}

class_obj = {
    "class": "inversiones",
    "vectorizer": "none",  # Or "text2vec-cohere" or "text2vec-huggingface"
}

class_obj = {
    "class": "rentabilidad",
    "vectorizer": "none",  # Or "text2vec-cohere" or "text2vec-huggingface"
}