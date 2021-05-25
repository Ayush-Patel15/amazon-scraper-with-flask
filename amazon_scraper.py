import requests
from requests.compat import urljoin
from bs4 import BeautifulSoup
import random
from user_agents_list import USER_AGENTS
from pprint import pprint

AMAZON_BASE_URL = "https://www.amazon.in/s"


def get_soup(url,headers= {}, params=[]):
    print("Getting: ", url)
    if "user-agent" not in headers:
        headers["user-agent"] = random.choice(USER_AGENTS)
    soup = BeautifulSoup(requests.get(
            url,
            headers=headers,
            params=params
        ).text,
        "lxml"
    )
    return soup

def scrape(query):
    response = get_soup(
        AMAZON_BASE_URL,
        params=[("k",query)]
    )
    links = []
    tags = response.select("a.a-text-normal")
    for tag in tags:
        links.append(tag["href"])
    return links

if __name__ == "__main__":
    pprint(scrape("shoes"))
