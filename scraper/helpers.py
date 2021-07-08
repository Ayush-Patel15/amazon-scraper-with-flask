import requests
from bs4 import BeautifulSoup
import random
from user_agents_list import USER_AGENTS

# a soup function that takes args as url,headers,parameters and return it lxml soup
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
