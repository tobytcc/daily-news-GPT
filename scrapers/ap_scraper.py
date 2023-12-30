"""
ap website scraper class, inherit from general article scraper
"""

from bs4 import BeautifulSoup, Tag

from scrapers.scrapers import ArticleScraper


class APArticleScraper(ArticleScraper):
    """ap scraper derived class"""

    CONFIG_FILE = "config/ap_config.yaml"
    SITE_NAME = "AP"

    def is_valid_category(self, category: list[str]) -> bool:
        """
        this function overwrites general is_valid_category base class implementation
        because special case, '/hub' is not a valid url extension
        """
        if category == ["hub"]:  # special case
            return False

        return super().is_valid_category(category)

    def _get_headline_from_tag(self, headline_tag: Tag) -> list[dict[str, str]]:
        parent1 = headline_tag.find_parent()

        # need to filter out the "trending" articles on top of webpage
        parent2 = parent1.find_parent("div", class_="PagePromo-title") if parent1 else None
        parent3 = parent2.find_parent("div", class_="PagePromo-content") if parent2 else None

        if parent1 and parent3 and "href" in parent1.attrs:
            href = parent1.attrs["href"]

            return [{"title": headline_tag.text.strip(), "path": href}]

        return []

    def _get_paragraphs_from_soup(self, article_soup: BeautifulSoup) -> list[str]:
        article_content = article_soup.find(name="div", attrs=self.article_config["attrs"])

        paragraph_list = []
        if isinstance(article_content, Tag):
            article_text_blocks = article_content.find_all(name="p")

            for text_block in article_text_blocks:
                if isinstance(text_block, Tag):
                    paragraph_list.append(text_block.text.strip())

        return paragraph_list
