import requests
from bs4 import BeautifulSoup

import yaml

class HTTPConnectionError(Exception):
    pass

def get_top_news_link(category: str, limit: int=3) -> list[dict[str, str]]:
    """
    returns a list of top headlines given the desired category

    category: category of news to to scrape headlines from
    limit: limit of headlines, default 3

    the scraping logic is that it seems like the extract is a headline
    iff the attr data-editable is headline, and its 3rd level parent is
    a hyperlink reference
    """

    with open('cnn_config.yaml', 'r') as config_file:
        cnn_config = yaml.safe_load(config_file)

    section_details = cnn_config['sections'][category]
    url = section_details['url']

    headline_list: list[dict[str, str]] = []

    response = requests.get(url)
    if response.status_code == 200:
        print('successfully connected to', url)
        soup = BeautifulSoup(response.content, 'html.parser')

        extracts = soup.find_all(attrs=section_details['attrs'])

        headlines_obtained = 0
        for extract in extracts:
            if headlines_obtained >= limit:
                return headline_list
            #all headlines seem to have href attribute as its 3rd level parents
            parent_1 = extract.find_parent()
            parent_2 = parent_1.find_parent() if parent_1 else None
            parent_3 = parent_2.find_parent() if parent_2 else None

            if parent_3 and parent_3.name == 'a' and 'href' in parent_3.attrs:
                href = parent_3.attrs['href']
                headline_list.append({'title': extract.text.strip(), 'path': href})

                headlines_obtained += 1

    else:
        raise HTTPConnectionError(
            f"Failed to connect to {url}. Status code: {response.status_code}"
        )

    return headline_list


def get_article_text(path: str) -> list[str]:
    """
    given a hyperlink to a cnn article, return the paragraphs as list.

    path: path to append to domain https://www.cnn.com/ to access article

    the scraping logic is that it seems like all pargraphs from the articles come
    from paragraph attributes with parent of class 'article__cnontent'.
    """
    with open('cnn_config.yaml', 'r') as config_file:
        cnn_config = yaml.safe_load(config_file)

    base_url = cnn_config['base_url']
    url = base_url + path

    article_config = cnn_config['article']

    paragraph_list: list[str] = []

    response = requests.get(url)
    if response.status_code == 200:
        print('successfully connected to', url)
        soup = BeautifulSoup(response.content, 'html.parser')

        article_content = soup.find(name='div', attrs=article_config['attrs'])

        paragraph_list = [p_obj.text.strip() for p_obj in article_content.find_all(name = 'p')]

    else:
        raise HTTPConnectionError(
            f"Failed to connect to {url}. Status code: {response.status_code}"
        )

    return paragraph_list
