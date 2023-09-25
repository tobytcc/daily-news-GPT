"""
this module runs the facebook/bart-large-cnn text summarizer on articles
"""

from transformers import pipeline

from cnn_scraper import get_articles

test_article = get_articles("world", 1)[0]

test_article_text = "\n".join(test_article.text)  # pylint: disable=invalid-name

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

print(test_article)
print(test_article_text)
print(summarizer(test_article_text, max_length=130, min_length=30, do_sample=False))
