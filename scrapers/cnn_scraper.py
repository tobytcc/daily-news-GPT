"""
this module contains helper functions to scrape CNN
"""

from urllib.parse import urljoin
from bs4 import Tag
import yaml

from scrapers.scrape_helper import make_request
from models.data_models import Article

CONFIG_FILE = "config/cnn_config.yaml"


def get_top_news(category: str, limit: int = 3) -> list[dict[str, str]]:
    """
    returns a list of top headlines title and paths given the desired category
    in a dictionary format.

    category: category of news to to scrape headlines from
    limit: limit of headlines, default 3

    the scraping logic is that it seems like the extract is a headline
    iff the attr data-editable is headline, and its 3rd level parent is
    a hyperlink reference
    """

    with open(CONFIG_FILE, "r", encoding="UTF-8") as config_file:
        cnn_config = yaml.safe_load(config_file)

    section_details = cnn_config["sections"][category]
    url = section_details["url"]

    headline_list: list[dict[str, str]] = []

    soup = make_request(url)
    extracts = soup.find_all(attrs=section_details["attrs"])

    headlines_obtained = 0
    for extract in extracts:
        if headlines_obtained >= limit:
            return headline_list

        # all headlines seem to have href attribute as its 3rd level parents
        parent = extract.find_parent()
        parent = parent.find_parent() if parent else None
        parent = parent.find_parent() if parent else None

        if parent and parent.name == "a" and "href" in parent.attrs:
            href = parent.attrs["href"]
            headline_list.append({"title": extract.text.strip(), "path": href})

            headlines_obtained += 1

    return headline_list


def get_article_text(path: str) -> list[str]:
    """
    given a hyperlink to a cnn article, return the paragraphs as list.

    path: path to append to domain https://www.cnn.com/ to access article

    the scraping logic is that it seems like all pargraphs from the articles come
    from paragraph attributes with parent of class 'article__cnontent'.
    """
    with open(CONFIG_FILE, "r", encoding="UTF-8") as config_file:
        cnn_config = yaml.safe_load(config_file)

    base_url = cnn_config["base_url"]
    url = urljoin(base_url, path)

    article_config = cnn_config["article"]

    paragraph_list: list[str] = []

    soup = make_request(url)

    article_content = soup.find(name="div", attrs=article_config["attrs"])

    if isinstance(article_content, Tag):
        paragraph_list = [p_obj.text.strip() for p_obj in article_content.find_all(name="p")]

    return paragraph_list


def get_articles(category: str, limit: int = 3) -> list[Article]:
    """
    returns a list of Article objects storing path, title, and paragraph texts from the
    given category, with length no more than limit.

    category: category within cnn to scrape articles from
    limit: the maximum number of articles to scrape
    """
    article_list = []

    top_news_list = get_top_news(category, limit)
    for news in top_news_list:
        paragraphs = get_article_text(news["path"])
        article_list.append(Article(path=news["path"], title=news["title"], text=paragraphs))

    return article_list
