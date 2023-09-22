import requests
from bs4 import BeautifulSoup

import yaml

class HTTPConnectionError(Exception):
    pass

def get_top_news_link(category: str, limit: int=3) -> list[tuple[str, str]]:
    with open('cnn_config.yaml', 'r') as config_file:
        cnn_config = yaml.safe_load(config_file)

    section_details = cnn_config['sections'][category]
    URL = section_details['url']

    headline_list: list[tuple[str, str]] = []

    response = requests.get(URL)
    if response.status_code == 200:
        print('successfully connected to', URL)
        soup = BeautifulSoup(response.content, 'html.parser')

        extracted_headlines = soup.find_all(attrs=section_details['attrs'])

        headlines_obtained = 0
        for headline in extracted_headlines:
            if headlines_obtained >= limit:
                return headline_list
            #all headlines seem to have href attribute as its 3rd level parents
            parent_1 = headline.find_parent()
            parent_2 = parent_1.find_parent() if parent_1 else None
            parent_3 = parent_2.find_parent() if parent_2 else None

            if parent_3 and parent_3.name == 'a' and 'href' in parent_3.attrs:
                href = parent_3.attrs['href']
                headline_list.append((headline.text.strip(), href))

                headlines_obtained += 1
        return headline_list

    else:
        raise HTTPConnectionError(
            f"Failed to connect to {URL}. Status code: {response.status_code}"
        )

    return []
