from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import openai

openai.api_type = "azure"
openai.api_base = "https://aisksamidev.openai.azure.com/"
openai.api_version = "2023-03-15-preview"

def generate_embeding(data):
    result = openai.Embedding.create(
        input=[data], engine="embedding-eagle-dev")
    return result.data[0].embedding

def vectoriezer(textInput):
    return generate_embeding(textInput)
    # vectorizer = TfidfVectorizer()
    # vector_generate = vectorizer.fit_transform([textInput]).toarray()
    # #print(vectorizer.vocabulary_)
    # return  np.pad(np.ravel(vector_generate, (0, 2000-len(vector_generate)), mode='constant') )
