from cnn_scrape_helper import get_top_news_link, HTTPConnectionError

try:
    top_news_links = get_top_news_link('US')
except HTTPConnectionError as e:
    print(e)

print(top_news_links)
