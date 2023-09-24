"""
this module contains the main logic for scraping cnn
test module, will integrate to other module later
"""

from cnn_helper import get_top_news_link, get_article_text

top_news_links = get_top_news_link("us", limit=3)
for news_item in top_news_links:
    print(news_item["path"])

if top_news_links:
    article_path = top_news_links[0]["path"]
    paragraphs = get_article_text(article_path)

if paragraphs:
    print(paragraphs[0])
