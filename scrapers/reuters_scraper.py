"""
this module contains helper functions to scrape BBC
"""

from typing import Union
from urllib.parse import urljoin
from bs4 import Tag

import yaml

from scrapers.scrape_helper import make_request

from models.data_models import Article

CONFIG_FILE = "config/ap_config.yaml"


def get_top_news(cat: str, limit: int = 3) -> list[dict[str, str]]:
    """
    returns a list of top headlines title and paths given the desired category
    in a dictionary format.

    category: category of news to to scrape headlines from
    limit: limit of headlines, default 3
    """

    with open(CONFIG_FILE, "r", encoding="UTF-8") as config_file:
        reuters_config = yaml.safe_load(config_file)

    section_details = reuters_config["sections"][cat]

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

        # need to filter out the "trending" articles on top of webpage
        grand_grandparent = parent.find_parent("div", class_="PagePromo-title").find_parent(
            "div", class_="PagePromo-content"
        )

        if parent and grand_grandparent and "href" in parent.attrs:
            href = parent.attrs["href"]

            headline = {"title": extract.text.strip(), "path": href}
            if headline not in headline_list:
                headline_list.append(headline)
                headlines_obtained += 1

    return headline_list


def get_article_text(path: str) -> list[str]:
    """
    given a hyperlink to a AP article, return the paragraphs as list.

    path: path to append to domain https://www.reuters.com/ to access article
    """
    with open(CONFIG_FILE, "r", encoding="UTF-8") as config_file:
        reuters_config = yaml.safe_load(config_file)

    base_url = reuters_config["base_url"]
    url = urljoin(base_url, path)

    paragraph_list: list[str] = []

    soup = make_request(url)

    article_content = soup.find(name="div", attrs={"class": "RichTextStoryBody RichTextBody"})

    if isinstance(article_content, Tag):
        article_text_blocks = article_content.find_all(name="p")

        for text_block in article_text_blocks:
            if isinstance(text_block, Tag):
                paragraph_list.append(text_block.text.strip())

    return paragraph_list


def get_articles(cat: str, limit: int = 3) -> list[Article]:
    """
    returns a list of Article objects storing path, title, and paragraph texts from the
    given category, with length no more than limit.

    category: category within cnn to scrape articles from
    limit: the maximum number of articles to scrape
    """
    article_list = []

    top_news_list = get_top_news(cat, limit)
    for news in top_news_list:
        paragraphs = get_article_text(news["path"])
        article_list.append(Article(path=news["path"], title=news["title"], text=paragraphs))

    return article_list
