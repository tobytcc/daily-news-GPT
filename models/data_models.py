"""
data_models module contains all useful data models for this project
"""


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
