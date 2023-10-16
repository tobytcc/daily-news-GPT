"""general scraper module, currently only contains article scraper class"""
import logging
from typing import Any, cast

from abc import ABC, abstractmethod
from urllib.parse import urljoin
from bs4 import BeautifulSoup

import yaml

from scrapers.scrape_helper import make_request
from models.data_models import Article

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ArticleScraper(ABC):
    """
    Base class for scraping all kinds of articles, with functions providing backbone structure
    """

    # typehint dummy variables
    _config: dict[str, Any]
    CONFIG_FILE: str
    SITE_NAME: str

    def __init__(self) -> None:
        self._config = self._load_config()
        self.sections_config = self._get_section_config()
        self.article_config = self._get_article_config()
        self.category_config = self._get_categories_config()
        self.aliases = self._get_alias_dict()
        self.base_url = self._get_base_url()

    def _load_config(self) -> dict[str, Any]:
        """loads [website]_config.yaml file for given [website] if successful"""
        try:
            with open(self.CONFIG_FILE, "r", encoding="UTF-8") as file:
                config = yaml.safe_load(file)
                return cast(dict[str, Any], config)
        except Exception as error:  # pylint: disable=broad-exception-caught
            logger.error("Error loading config: %s", error)
            return {}

    def _get_base_url(self) -> str:
        """return base url for given website"""
        return cast(str, self._config["base_url"])

    def _get_section_config(self) -> dict[str, Any]:
        """returns section configuration dict for given website"""
        return cast(dict[str, Any], self._config["sections"])

    def _get_article_config(self) -> dict[str, Any]:
        """returns article configuration dict for given website"""
        return cast(dict[str, Any], self._config["article"])

    def _get_categories_config(self) -> dict[str, Any]:
        """returns categories configuration dict for given website"""
        return cast(dict[str, Any], self._config["categories"])

    def _get_alias_dict(self) -> dict[str, Any]:
        """returns alias dict for given website"""
        return cast(dict[str, str], self._config["aliases"])

    def _resolve_category_alias(self, category: list[str]) -> list[str]:
        """converts alias to the appropriate categories to access website"""
        if self.aliases is None:
            return category

        return [self.aliases.get(cat, cat) for cat in category]

    def _get_top_news(self, category: list[str], limit: int) -> list[dict[str, str]]:
        """
        returns a list of top headlines title and paths given the desired category
        in a dictionary format.

        category: category of news to to scrape headlines from. if list len > 1, means
        subcategories exist, joined by "/"
        limit: limit of headlines, default 3
        """
        category = self._resolve_category_alias(category)

        if not self.is_valid_category(category):
            raise ValueError(f"invalid category: '{'/'.join(category)}' in site: {self.SITE_NAME}")

        url = self.base_url
        for cat in category:
            if not cat.endswith("/"):
                cat += "/"
            url = urljoin(url, cat)

        soup = make_request(url)

        return self._get_top_news_from_soup(soup, limit)

    # def _get_top_news_from_soup(
    #     self, section_soup: BeautifulSoup, limit: int
    # ) -> list[dict[str, str]]:
    #     """
    #     this function could be overwritten if a website structure involves
    #     something other than a .find_all to get top headlines
    #     """
    #     extracts = section_soup.find_all(attrs=self.sections_config["attrs"])
    #     headline_list: list[dict[str, str]] = []
    #     for extract in extracts:

    def _get_article_text(self, path: str) -> list[str]:
        """
        given a hyperlink to an article, return the paragraphs as list.
        """
        base_url = self.base_url
        url = urljoin(base_url, path)

        soup = make_request(url)

        return self._get_paragraphs_from_soup(soup)

    def is_valid_category(self, category: list[str]) -> bool:
        """
        determines if the given category list is valid html hyperlink append
        e.g. ["news", world"] is a valid category for bbc because we can parse
        bbc.com/news/world
        """
        category_search = self.category_config

        for cat in category:
            if (category_search is None) or (cat not in category_search):
                return False
            category_search = category_search[cat]

        return True

    def get_articles(self, category: list[str], limit: int = 3) -> list[Article]:
        """
        returns a list of Article objects storing path, title, and paragraph texts from the
        given category, with length no more than limit.
        """
        article_list = []

        top_news_list = self._get_top_news(category, limit)
        for news in top_news_list:
            paragraphs = self._get_article_text(news["path"])
            article_list.append(Article(path=news["path"], title=news["title"], text=paragraphs))

        return article_list

    @abstractmethod
    def _get_top_news_from_soup(
        self, section_soup: BeautifulSoup, limit: int
    ) -> list[dict[str, str]]:
        """extract top news headline title & path using specific scraping logic for that website"""
        raise NotImplementedError("article specific scraping logic not defined")

    @abstractmethod
    def _get_paragraphs_from_soup(self, article_soup: BeautifulSoup) -> list[str]:
        """extract paragraph text using specific scraping logic for that website"""
        raise NotImplementedError("article specific scraping logic not defined")
