"""
bbc website scraper class, inherit from general article scraper
"""

from bs4 import BeautifulSoup, Tag

from scrapers.scrapers import ArticleScraper


class BBCArticleScraper(ArticleScraper):
    """bbc scraper derived class"""

    CONFIG_FILE = "config/bbc_config.yaml"
    SITE_NAME = "BBC"

    def _get_headline_from_tag(self, headline_tag: Tag) -> list[dict[str, str]]:
        # seem to have href attribute as its 1st level parents
        parent = headline_tag.find_parent()

        if parent and parent.name == "a" and "href" in parent.attrs:
            href = parent.attrs["href"]

            # filter out live article, as I don't know how to scrape it yet
            if "live" in href.split("/"):
                return []

            return [{"title": headline_tag.text.strip(), "path": href}]

        return []

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
