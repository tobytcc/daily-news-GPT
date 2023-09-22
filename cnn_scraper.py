from cnn_scrape_helper import get_top_news_link, HTTPConnectionError

try:
    top_news_links = get_top_news_link('US')
except HTTPConnectionError as e:
    print(e)

for news in top_news_links:
    print(news)
