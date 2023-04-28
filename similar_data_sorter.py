from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import weaviate

client = weaviate.Client(url="https://moviexpredeitor-77pe0djc.weaviate.network")

financial_keywords = ["cdt", "inversiones", "rentabilidad"]

documents = [
    "CDT CDT CDT CDT CDT CDT CDT CDT CDT cdt cdt cdt",
    "Este es un ejemplo inversiones",
    "inversiones inversiones inversiones INverSIONES invrsion",
    "CDT inversiones Rentabilidad",
    "este no tiene nada ",
    "este no tiene nada ..... o si? Cdt cjt",
    "algo inversionesl",
    "//&)/%&/&%&/&%$#%&/()",
    "A DONDE CAIGA",
]


tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

kmeans = KMeans(n_clusters=3, random_state=0)
kmeans.fit(tfidf_matrix)

keyword_indices = [
    tfidf_vectorizer.vocabulary_[keyword] for keyword in financial_keywords
]

keyword_weights = tfidf_matrix[:, keyword_indices].toarray()

for i, document in enumerate(documents):
    with client.batch as batch:
        if keyword_weights[0] > 0.5:
            batch.add_data_object(
                document, financial_keywords[0], vector=tfidf_matrix[i]
            )
        if keyword_weights[1] > 0.5:
            batch.add_data_object(
                document, financial_keywords[1], vector=tfidf_matrix[i]
            )
        if keyword_weights[2] > 0.5:
            batch.add_data_object(
                document, financial_keywords[2], vector=tfidf_matrix[i]
            )
