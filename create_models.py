import weaviate

client = weaviate.Client(url="https://moviexpredeitor-77pe0djc.weaviate.network")
# client.schema.delete_all() #Si se desea eliminar todos los schemas

class_obj = {
    "class": "Movie",
    "vectorizer": "none",
}
client.schema.create_class(class_obj)


class_obj = {
    "class": "cdt",
    "vectorizer": "none",
}
client.schema.create_class(class_obj)


class_obj = {
    "class": "inversiones",
    "vectorizer": "none",
}
client.schema.create_class(class_obj)


class_obj = {
    "class": "rentabilidad",
    "vectorizer": "none",
}

class_obj = {
    "class": "CdtValidData",
    "vectorizer": "none",
}
client.schema.create_class(class_obj)


class_obj = {
    "class": "inversionesValidado",
    "vectorizer": "none",
}
client.schema.create_class(class_obj)

class_obj = {
    "class": "rentabilidadValidado",
    "vectorizer": "none",
}
client.schema.create_class(class_obj)