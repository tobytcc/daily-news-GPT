"""
this module would runs the facebook/bart-large-cnn text summarizer on articles

for now, its just here to run scraping and test them
"""
# pylint: disable=unused-import

# from transformers import pipeline

from scrapers.bbc_scraper import BBCArticleScraper
from scrapers.cnn_scraper import CNNArticleScraper
from scrapers.ap_scraper import APArticleScraper
from scrapers.abc_scraper import ABCArticleScraper

from helper import parse_categories

test = BBCArticleScraper()  # choose your scraper

# this parse_categories function is used to test if all categories in the yaml configs are valid
# it returns a list, each element being a category constructed from config file

# currently running main.py will just scrape 1 article per category for that specific news site
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
