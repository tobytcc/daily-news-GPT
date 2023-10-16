"""
this module contains helper functions to scrape ABC News
"""
from bs4 import BeautifulSoup, Tag

from scrapers.scrapers import ArticleScraper


class ABCArticleScraper(ArticleScraper):
    """abc scraper derived class"""

    CONFIG_FILE = "config/abc_config.yaml"
    SITE_NAME = "ABC"

    def _get_top_news_from_soup(
        self, section_soup: BeautifulSoup, limit: int
    ) -> list[dict[str, str]]:
        """
        todo
        """
        extracts = section_soup.find_all(attrs=self.sections_config["attrs"])
        headline_list: list[dict[str, str]] = []
        for extract in extracts:
            if len(headline_list) >= limit:
                return headline_list

            parent = extract.find_parent("a", class_="AnchorLink News News--xl")

            # two types of acceptable parents
            if parent is None:
                parent = extract.find_parent("a")

            if parent and "href" in parent.attrs:
                href = parent.attrs["href"]

                headline = {"title": extract.text.strip(), "path": href}
                if headline not in headline_list:
                    headline_list.append(headline)

        return headline_list

    def _get_paragraphs_from_soup(self, article_soup: BeautifulSoup) -> list[str]:
        article_content = article_soup.find(name="article", attrs=self.article_config["attrs"])

        paragraph_list = []
        if isinstance(article_content, Tag):
            article_text_blocks = article_content.find_all(class_="Ekqk")  # HIGHLY BUG-PRONE

            for text_block in article_text_blocks:
                if isinstance(text_block, Tag):
                    paragraph_list.append(text_block.text.strip())

        return paragraph_list
