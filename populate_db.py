import openai
import pandas as pd
import asyncio
import weaviate
client = weaviate.Client(url="https://moviexpredeitor-77pe0djc.weaviate.network")

openai.api_type = "azure"
openai.api_base = "https://aisksamidev.openai.azure.com/"
openai.api_version = "2023-03-15-preview"


movies_data = pd.read_csv("movies_all_data.csv")
movies_data.columns = ["id", "title", "tags", "vector"]


async def generate_embeding(i):
    result = await openai.Embedding.acreate(
        input=[movies_data.at[i, "tags"]], engine="embedding-eagle-dev"
    )
    movies_data.at[i, "vector"] = result.data[0].embedding
    return result.data[0].embedding


tasks = [generate_embeding(i) for i, row in movies_data.iterrows()]


async def main():
    embeddings_response = []
    max_query = 50
    delay_per_request = 15  # there is a 50/10sec rate limit in openai azure models
    for i in range(0, len(tasks), max_query):
        result = await asyncio.gather(*tasks[i : i + max_query])
        embeddings_response.extend(result)
        print(f"voy en la linea {i} ")
        await asyncio.sleep(delay_per_request)

    counter = 0
    client.batch.configure(batch_size=49, creation_time=12)
    with client.batch as batch:
        for i, article in movies_data.iterrows():
            if counter % 10 == 0:
                print(f"Import {counter} / {len(movies_data )} ")

            properties = {
                "title": article["title"],
                "idMovie": article["id"],
                "tags": article["tags"],
            }

            batch.add_data_object(properties, "Movie", vector=article["vector"])
            counter = counter + 1

    print("worker!!!")


asyncio.run(main())
