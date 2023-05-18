import openai
import os
import asyncio
import pandas as pd
import math

openai.api_type = "azure"
openai.api_base = "https://aisksamidev.openai.azure.com/"
openai.api_version = "2023-03-15-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")

num_data_obj = 5000
result_data = 1
#question = "crea un texto de tema cdt de entre 500 y 1000 palabras introducionde aleatoriamente la palabra cdt"

question = "crea un texto explicando que es cdt financiero de entre 500 y 1000 palabras "

async def call_api():
    delay_per_request = 300
    try:
        await asyncio.sleep(20)
        response = openai.ChatCompletion.create(
            engine="eagle-dev",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content":  question}
            ],
            n=50)
    except:
        await asyncio.sleep(delay_per_request)
        response = openai.ChatCompletion.create(
            engine="eagle-dev",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content":  question}
            ],
            n=50)

    return response


def get_data(response, index):
    lst = []
    for i, data in enumerate(response.choices):
        if 'content' in data['message']:
            lst.append(
                f"{data['message']['content']}")
    return lst


async def generate_data(index):
    lst = []
    response = await call_api()
    if (response):
        lst = get_data(response, index)

    print(f"va por la iteracion {index}")
    return lst


def save_data(lst):
    df = pd.DataFrame(lst, columns=['Valores'])
    df['valido'] = result_data
    df.to_excel('valores.xlsx', index=False)


async def main():
    try:
        lst = []
        for i in range(math.ceil(num_data_obj/50)):
            lst += await generate_data(i)
        save_data(lst)
    except:
        save_data(lst)
    print("guardo")


asyncio.run(main())
