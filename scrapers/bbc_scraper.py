"""
this module contains helper functions to scrape BBC
"""

from typing import Union

import yaml

from scrapers.scrape_helper import make_request

CONFIG_FILE = "config/bbc_config.yaml"


def get_top_news(cat: str, subcat: Union[str, None], limit: int = 3) -> list[dict[str, str]]:
    """
    returns a list of top headlines title and paths given the desired category
    in a dictionary format.

    category: category of news to to scrape headlines from
    limit: limit of headlines, default 3
    """

    with open(CONFIG_FILE, "r", encoding="UTF-8") as config_file:
        bbc_config = yaml.safe_load(config_file)

    section_details = bbc_config["sections"][cat]
    if isinstance(subcat, str):
        section_details = section_details[subcat]

    url = section_details["url"]

    headline_list: list[dict[str, str]] = []

    soup = make_request(url)
    extracts = soup.find_all(attrs=section_details["attrs"])

    headlines_obtained = 0
    for extract in extracts:
        if headlines_obtained >= limit:
            return headline_list

        # seem to have href attribute as its 1st level parents
        parent = extract.find_parent()

        if parent and parent.name == "a" and "href" in parent.attrs:
            href = parent.attrs["href"]

            headline = {"title": extract.text.strip(), "path": href}
            if headline not in headline_list:
                headline_list.append(headline)
                headlines_obtained += 1

    return headline_list
