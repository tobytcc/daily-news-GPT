import requests
from bs4 import BeautifulSoup

from cnn_scrape_helper import getTopNews


URL = 'https://www.cnn.com/us'

response = requests.get(URL)
if response.status_code == 200:
    print('successfully connected to', URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    top_news = getTopNews(soup)
    print(top_news)
else:
    print('failed to connect to', URL)
    print('status code: ', response.status_code)
