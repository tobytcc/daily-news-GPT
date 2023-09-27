"""
this module contains helper functions to scrape BBC
"""

from typing import Union
from urllib.parse import urljoin
from bs4 import Tag

import yaml

from scrapers.scrape_helper import make_request

from models.data_models import Article

CONFIG_FILE = "config/bbc_config.yaml"


def get_top_news(cat: str, subcat: Union[str, None], limit: int = 3) -> list[dict[str, str]]:
    """
    returns a list of top headlines title and paths given the desired category
    in a dictionary format.

    category: category of news to to scrape headlines from
    limit: limit of headlines, default 3
    """

    with open(CONFIG_FILE, "r", encoding="UTF-8") as config_file:
        bbc_config = yaml.safe_load(config_file)

    section_details = bbc_config["sections"][cat]
    if isinstance(subcat, str):
        section_details = section_details[subcat]

    url = section_details["url"]

    headline_list: list[dict[str, str]] = []

    soup = make_request(url)
    extracts = soup.find_all(attrs=section_details["attrs"])

    headlines_obtained = 0
    for extract in extracts:
        if headlines_obtained >= limit:
            return headline_list

        # seem to have href attribute as its 1st level parents
        parent = extract.find_parent()

        if parent and parent.name == "a" and "href" in parent.attrs:
            href = parent.attrs["href"]

            if "live" in href.split(
                "/"
            ):  # filter out live article, as I don't know how to scrape it
                continue

            headline = {"title": extract.text.strip(), "path": href}
            if headline not in headline_list:
                headline_list.append(headline)
                headlines_obtained += 1

    return headline_list


def get_article_text(path: str) -> list[str]:
    """
    given a hyperlink to a bbc article, return the paragraphs as list.

    path: path to append to domain https://www.bbc.com/ to access article
    """
    with open(CONFIG_FILE, "r", encoding="UTF-8") as config_file:
        bbc_config = yaml.safe_load(config_file)

    base_url = bbc_config["base_url"]
    url = urljoin(base_url, path)

    article_config = bbc_config["article"]

    paragraph_list: list[str] = []

    soup = make_request(url)

    article_content = soup.find(name="article")

    if isinstance(article_content, Tag):
        article_text_blocks = article_content.find_all(name="div", attrs=article_config["attrs"])

        for text_block in article_text_blocks:
            if isinstance(text_block, Tag):
                text_obj = text_block.find(name="p")
                if isinstance(text_obj, Tag):
                    paragraph_list.append(text_obj.text.strip())

    return paragraph_list


def get_articles(cat: str, subcat: Union[str, None], limit: int = 3) -> list[Article]:
    """
    returns a list of Article objects storing path, title, and paragraph texts from the
    given category, with length no more than limit.

    category: category within cnn to scrape articles from
    limit: the maximum number of articles to scrape
    """
    article_list = []

    top_news_list = get_top_news(cat, subcat, limit)
    for news in top_news_list:
        paragraphs = get_article_text(news["path"])
        article_list.append(Article(path=news["path"], title=news["title"], text=paragraphs))

    return article_list
