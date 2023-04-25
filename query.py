import weaviate
import openai

openai.api_type = "azure"
openai.api_base = "https://aisksamidev.openai.azure.com/"
openai.api_version = "2023-03-15-preview"

client = weaviate.Client(
    url="https://moviexpredeitor-77pe0djc.weaviate.network"
)


def generate_embeding(data):
    result = openai.Embedding.create(
        input=[data], engine="embedding-eagle-dev")
    return result.data[0].embedding

result =client.query .get("Movie",["idMovie","title"]).with_near_vector({"vector": generate_embeding("commedy")}).with_limit(15).do()
print(result)