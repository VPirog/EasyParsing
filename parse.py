import pandas as pd  # library for data analysis
import requests  # library to handle requests
from tqdm import tqdm
from bs4 import BeautifulSoup  # library to parse HTML documents
import os
import asyncio
import aiohttp


def parsing(wikiurl):
    table_class = "wikitable sortable"
    response = requests.get(wikiurl)
    # print(response.status_code)

    if (response.status_code == 200):
        print("Успешное подключение")

    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': "wikitable"})

    df = pd.read_html(str(table))
    # convert list to dataframe
    df = pd.DataFrame(df[0])
    # print(df)
    os.makedirs('parse_out',
                exist_ok=True)  # создаем директорию со всеми промежуточными каталогами, если они не существуют
    with open('parse_out/out.csv', 'w+'):
        df.to_csv('parse_out/out.csv')
    with open('parse_out/out.xlsx', 'w+'):
        df.to_excel('parse_out/out.xlsx', sheet_name='Sheet_name_1')

    # # drop the unwanted columns
    # data = df.drop(["Rank", "Population(2001)"], axis=1)
    # # rename columns for ease
    # data = data.rename(columns={"City": "Neighborhood","State or union territory": "State","Population(2011)[3]": "Population"})
    # data.head()


async def download_image(session, url, name):
    try:
        async with session.get(url) as response:
            with open(f"parse_out/img/{name}", "wb") as f:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)
    except Exception as e:
        print(f"Error while downloading {url}: {e}")


from urllib.parse import urljoin

...

async def parsing_image(url):
    async with aiohttp.ClientSession() as session:
        while True:
            response = await session.get(url)
            soup = BeautifulSoup(await response.text(), "html.parser")
            images = soup.find_all("img", class_="lazyload")
            if not images:
                break
            os.makedirs("parse_out/img", exist_ok=True)
            tasks = []
            for image in images:
                image_url = image['data-src']
                image_name = image['data-image-name']
                image_url = urljoin(url, image_url)  # исправление ссылки
                tasks.append(download_image(session, image_url, image_name))
            await asyncio.gather(*tasks)
            next_page = soup.find("a", text="next page")
            if not next_page:
                break
            url = urljoin(url, next_page['href'])  # исправление ссылки

