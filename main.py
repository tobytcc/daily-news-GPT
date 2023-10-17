"""
this module runs the facebook/bart-large-cnn text summarizer on articles

for now, its just here to run scraping though
"""
# pylint: disable=unused-import

# from transformers import pipeline

from scrapers.bbc_scraper import BBCArticleScraper
from scrapers.cnn_scraper import CNNArticleScraper
from scrapers.ap_scraper import APArticleScraper
from scrapers.abc_scraper import ABCArticleScraper

from helper import parse_categories

# testbbc = BBCArticleScraper()
# bbc = testbbc.get_articles(category=["news"])
# print("bbc articles:", len(bbc))
# for article in bbc:
#     print(article)

# testcnn = CNNArticleScraper()
# cnn = testcnn.get_articles(category=["world"])
# print("cnn articles:", len(cnn))
# for article in cnn:
#     print(article)

test = ABCArticleScraper()

cat_list = parse_categories(test.category_config)

print(cat_list)

for cat in cat_list:
    try:
        articles = test.get_articles(category=cat, limit=1)
    except ValueError:
        continue
    print("articles:", len(articles))
    for article in articles:
        print(article)
