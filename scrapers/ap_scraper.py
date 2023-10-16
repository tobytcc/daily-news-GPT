"""
this module contains helper functions to scrape AP
"""

from bs4 import BeautifulSoup, Tag

from scrapers.scrapers import ArticleScraper


class APArticleScraper(ArticleScraper):
    """bbc scraper derived class"""

    CONFIG_FILE = "config/ap_config.yaml"
    SITE_NAME = "AP"

    def is_valid_category(self, category: list[str]) -> bool:
        """
        special case, 'hub' is not a valid url extension
        """
        if category == ["hub"]:  # special case
            return False

        return super().is_valid_category(category)

    def _get_top_news_from_soup(
        self, section_soup: BeautifulSoup, limit: int
    ) -> list[dict[str, str]]:
        extracts = section_soup.find_all(attrs=self.sections_config["attrs"])

        headline_list: list[dict[str, str]] = []
        for extract in extracts:
            if len(headline_list) >= limit:
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

        return headline_list

    def _get_paragraphs_from_soup(self, article_soup: BeautifulSoup) -> list[str]:
        """
        defaultext
        """
        article_content = article_soup.find(name="div", attrs=self.article_config["attrs"])

        paragraph_list = []
        if isinstance(article_content, Tag):
            article_text_blocks = article_content.find_all(name="p")

            for text_block in article_text_blocks:
                if isinstance(text_block, Tag):
                    paragraph_list.append(text_block.text.strip())

        return paragraph_list
