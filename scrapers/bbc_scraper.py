"""bbc scraper class"""
from bs4 import BeautifulSoup, Tag

from scrapers.scrapers import ArticleScraper


class BBCArticleScraper(ArticleScraper):
    """bbc scraper derived class"""

    CONFIG_FILE = "config/bbc_config.yaml"
    SITE_NAME = "BBC"

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

            if parent and parent.name == "a" and "href" in parent.attrs:
                href = parent.attrs["href"]

                if "live" in href.split(
                    "/"
                ):  # filter out live article, as I don't know how to scrape it
                    continue

                headline = {"title": extract.text.strip(), "path": href}
                if headline not in headline_list:
                    headline_list.append(headline)

        return headline_list

    def _get_paragraphs_from_soup(self, article_soup: BeautifulSoup) -> list[str]:
        paragraph_list = []

        article_content = article_soup.find(name="article")
        if isinstance(article_content, Tag):
            article_text_blocks = article_content.find_all(
                name="div", attrs=self.article_config["attrs"]
            )

            for text_block in article_text_blocks:
                if isinstance(text_block, Tag):
                    text_obj = text_block.find(name="p")
                    if isinstance(text_obj, Tag):
                        paragraph_list.append(text_obj.text.strip())

        return paragraph_list
