from bs4 import BeautifulSoup

def getTopNews(soup: BeautifulSoup) -> list[str]:

    top_news_parents = soup.find_all('div',
                                attrs = {
                                    'class': ' '.join(['container__title', 'container_lead-plus-headlines__title',
                                              'container__title--emphatic', 'hover', 'container__title--emphatic-size-l2']),
                                    'data-editable': 'titleLink'
                                    })

    titles = []
    for top_news_parent in top_news_parents:
        if top_news_parent:
            top_news = top_news_parent.find_all(name= 'h2')

            for news in top_news: #likely only 1
                titles.append(news.text.strip())

    return titles
