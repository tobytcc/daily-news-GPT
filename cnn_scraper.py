"""
this module contains main function which scrapes n top news from user input category
"""

from cnn_helper import get_top_news, get_article_text


class Article:
    """
    Article class, stores path, title, and text of article.
    (subject to more addition in future, e.g. images?)
    """

    def __init__(self, path: str, title: str, text: list[str]):
        self.path = path
        self.title = title
        self.text = text

    def __str__(self) -> str:
        output = "path: " + self.path + "\n"
        output += "title: " + self.title + "\n"
        output += "paragraphs in article: " + str(len(self.text)) + "\n"

        return output

    def __repr__(self) -> str:
        return f"Article(path='{self.path}', title='{self.title}', text={self.text})"


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
