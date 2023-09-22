from bs4 import BeautifulSoup

import yaml

def getTopNews(soup: BeautifulSoup, category: str = "", limit: int=3) -> list[tuple[str, str]]:

    extracted_headlines = soup.find_all(attrs={"data-editable": 'headline'})

    headlines_obtained = 0
    headline_list: list[tuple[str,str]] = []
    for headline in extracted_headlines:
        if headlines_obtained >= limit:
            return headline_list
        #all headlines seem to have href attribute as its 3rd level parents
        parent_1 = headline.find_parent()
        parent_2 = parent_1.find_parent() if parent_1 else None
        parent_3 = parent_2.find_parent() if parent_2 else None

        if parent_3 and parent_3.name == 'a' and 'href' in parent_3.attrs:
            href = parent_3.attrs['href']
            headline_list.append((headline.text.strip(), href))

            headlines_obtained += 1

    return headline_list
