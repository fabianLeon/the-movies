import weaviate
import openai
import pandas as pd
import numpy as np
import asyncio

openai.api_type = "azure"
openai.api_base = "https://aisksamidev.openai.azure.com/"
openai.api_version = "2023-03-15-preview"

client = weaviate.Client(
    url="https://moviexpredeitor-77pe0djc.weaviate.network"
)


class_obj = {
    "class": "Movie",
    "vectorizer": "none"  # Or "text2vec-cohere" or "text2vec-huggingface"
}
client.schema.delete_all()
client.schema.create_class(
    class_obj
)

movies_data = pd.read_csv("movies_all_data.csv")
movies_data.columns = ["id", "title", "tags"]
movies_data["vector"] = 0


def generate_embeding(row):
    result = openai.Embedding.create(
        input=[row["tags"]], engine="embedding-eagle-dev")
    row["vector"] = result.data[0].embedding
    return result.data[0].embedding


tasks = [generate_embeding(row) for i, row in movies_data.iterrows()]


async def main():
    embeddings_response = []
    max_query = 50
    delay_per_request = 15  # there is a 50/10sec rate limit in openai azure models
    for i in range(0, len(tasks), max_query):
        result = await asyncio.gather(*tasks[i:i+max_query])
        embeddings_response.extend(result)
        print(f"voy en la linea {i} que es {result[0]['title']}")
        await asyncio.sleep(delay_per_request)

    counter = 0
    client.batch.configure(batch_size=49, creation_time=12)
    with client.batch as batch:
        for i, article in movies_data.iterrows():
            if (counter % 10 == 0):
                print(f"Import {counter} / {len(movies_data )} ")

            properties = {
                "title": article["title"],
                "idMovie": article["id"],
                "tags": article["tags"]
            }

            batch.add_data_object(properties, "Movie",
                                  vector=article["vector"])
            counter = counter+1

    print("worker!!!")


asyncio.run(main())
