"""
this module runs the facebook/bart-large-cnn text summarizer on articles
"""

# from transformers import pipeline

from scrapers.cnn_scraper import get_articles as cnn_get_articles
from scrapers.bbc_scraper import get_articles as bbc_get_articles
from scrapers.abc_scraper import get_articles as abc_get_articles
from scrapers.ap_scraper import get_articles as ap_get_articles

test_article = ap_get_articles("world", 3)

for x in test_article:
    print(x)

test_article_text = "\n".join(test_article.text)  # pylint: disable=invalid-name

# summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

print(test_article)
# print(test_article_text)
# print(summarizer(test_article_text, max_length=130, min_length=30, do_sample=False))
