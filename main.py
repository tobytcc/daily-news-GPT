"""
this module runs the facebook/bart-large-cnn text summarizer on articles
"""

# from transformers import pipeline

from scrapers.bbc_scraper import BBCArticleScraper
from scrapers.cnn_scraper import CNNArticleScraper

testbbc = BBCArticleScraper()
bbc = testbbc.get_articles(category=["news"])
print("bbc articles:", len(bbc))
for article in bbc:
    print(article)

testcnn = CNNArticleScraper()
cnn = testcnn.get_articles(category=["world", "what"])
print("cnn articles:", len(cnn))
for article in cnn:
    print(article)
