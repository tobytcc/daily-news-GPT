"""
abc website scraper class, inherit from general article scraper
"""

from bs4 import BeautifulSoup, Tag

from scrapers.scrapers import ArticleScraper


class ABCArticleScraper(ArticleScraper):
    """abc scraper derived class"""

    CONFIG_FILE = "config/abc_config.yaml"
    SITE_NAME = "ABC"

    def _get_headline_from_tag(self, headline_tag: Tag) -> list[dict[str, str]]:
        parent = headline_tag.find_parent("a", class_="AnchorLink News News--xl")

        # two types of acceptable parents
        if parent is None:
            parent = headline_tag.find_parent("a")

        if parent and "href" in parent.attrs:
            href = parent.attrs["href"]

            return [{"title": headline_tag.text.strip(), "path": href}]

        return []

    def _get_paragraphs_from_soup(self, article_soup: BeautifulSoup) -> list[str]:
        article_content = article_soup.find(name="article", attrs=self.article_config["attrs"])

        paragraph_list = []
        if isinstance(article_content, Tag):
            article_text_blocks = article_content.find_all(class_="Ekqk")  # HIGHLY BUG-PRONE

            for text_block in article_text_blocks:
                if isinstance(text_block, Tag):
                    paragraph_list.append(text_block.text.strip())

        return paragraph_list
