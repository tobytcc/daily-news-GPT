"""
cnn website scraper class, inherit from general article scraper
"""

from bs4 import BeautifulSoup, Tag

from scrapers.scrapers import ArticleScraper


class CNNArticleScraper(ArticleScraper):
    """cnn scraper derived class"""

    CONFIG_FILE = "config/cnn_config.yaml"
    SITE_NAME = "CNN"

    def _get_headline_from_tag(self, headline_tag: Tag) -> list[dict[str, str]]:
        # all headlines seem to have href attribute as its 3rd level parents
        parent = headline_tag.find_parent()
        parent = parent.find_parent() if parent else None
        parent = parent.find_parent() if parent else None

        if parent and parent.name == "a" and "href" in parent.attrs:
            href = parent.attrs["href"]
            return [{"title": headline_tag.text.strip(), "path": href}]

        return []

    def _get_paragraphs_from_soup(self, article_soup: BeautifulSoup) -> list[str]:
        paragraph_list = []

        article_content = article_soup.find(name="div", attrs=self.article_config["attrs"])
        if isinstance(article_content, Tag):
            paragraph_list = [p_obj.text.strip() for p_obj in article_content.find_all(name="p")]

        return paragraph_list
