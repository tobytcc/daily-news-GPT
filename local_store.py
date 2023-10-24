"""
this module would runs the facebook/bart-large-cnn text summarizer on articles

for now, its just here to run scraping and test them
"""
# pylint: disable=unused-import

# from transformers import pipeline

import time



from scrapers.bbc_scraper import BBCArticleScraper
from scrapers.cnn_scraper import CNNArticleScraper
from scrapers.ap_scraper import APArticleScraper
from scrapers.abc_scraper import ABCArticleScraper
from csv import writer

from helper import parse_categories

BBCScraper = BBCArticleScraper()
CNNScraper = CNNArticleScraper()
APScraper = APArticleScraper()
ABCScraper = ABCArticleScraper()  # choose your scraper

scraper_dict = {"BBC": BBCScraper, "CNN": CNNScraper, "AP": APScraper, "ABC": ABCScraper}

# this parse_categories function is used to test if all categories in the yaml configs are valid
# it returns a list, each element being a category constructed from config file

# currently running main.py will just scrape 1 article per category for that specific news site
with open("articles.csv", 'a') as f:
    writer_object = writer(f)

    for site, scraper in scraper_dict.items():    
        
        cat_list = parse_categories(scraper.category_config)

        print(cat_list)

        for cat in cat_list:
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            print(current_time)

            try:
                articles = scraper.get_articles(category=cat, limit=1)
            except ValueError:
                continue

            print("articles:", len(articles))
            for article in articles:
                print(article)
                field = "_".join([site, cat])
                new_row = [current_time, field, article.title, article.text]
                # Writing into file
                writer_object.writerow(new_row)


f.close()