import tensorflow as tf
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences

# Corpus de ejemplo
corpus = [
    "Este es el primer documento.",
    "Este es el segundo documento.",
    "Y este es el tercer documento.",
    "Este es el último documento.",
]

# Crear una instancia del tokenizador
tokenizer = Tokenizer()

# Ajustar el tokenizador al corpus
tokenizer.fit_on_texts(corpus)

# Convertir el corpus en secuencias de enteros
sequences = tokenizer.texts_to_sequences(corpus)

# Padding de las secuencias para tener la misma longitud
maxlen = max([len(seq) for seq in sequences])
padded_sequences = pad_sequences(sequences, maxlen=maxlen, padding="post")

# Crear el modelo de Word Embeddings
model = tf.keras.models.Sequential(
    [
        tf.keras.layers.Embedding(
            input_dim=len(tokenizer.word_index) + 1, output_dim=10, input_length=maxlen
        ),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(1, activation="sigmoid"),
    ]
)

# Compilar y ajustar el modelo
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
model.fit(padded_sequences, [0, 0, 1, 1], epochs=50, verbose=0)

# Obtener los vectores de Word Embeddings
embeddings = model.layers[0].get_weights()[0]
word_index = tokenizer.word_index

# Imprimir el vector de Word Embeddings para la palabra 'documento'
print(embeddings[word_index["documento"]])
