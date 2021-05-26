import requests
from urllib.parse import urljoin
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

def get_links(query):
    response = get_soup(
        AMAZON_BASE_URL,
        params=[("k",query)]
    )
    links = []
    tags = response.select("a.a-text-normal")
    for tag in tags:
        links.append(tag["href"])
    return links

def get_details(link):
    response = get_soup(
        urljoin(AMAZON_BASE_URL, link)
    )
    try:
        details_section = response.select('#centerCol')[0]
        url = urljoin(AMAZON_BASE_URL,link)
        title = details_section.select('#productTitle')[0].text.strip()
        brand = details_section.select('#bylineInfo')[0].text
        availability = details_section.select("#availability")[0].text.strip()
        description = details_section.select('#feature-bullets')[0].select(".a-list-item")
        emi = details_section.select("#inemi_feature_div")[0].select("span")[0].text
        sold_by = details_section.select("#sellerProfileTriggerId")[0].text
        rating_stars = details_section.select("#acrPopover")[0]["title"]
        total_raitngs = details_section.select("#acrCustomerReviewText")[0].text
        if details_section.select('#priceblock_ourprice'):
            price = details_section.select('#priceblock_ourprice')[0].text
        elif details_section.select('#priceblock_dealprice'):
            price = details_section.select('#priceblock_dealprice')[0].text
        else:
            price = 'NA'
        try:
            price = price.replace("\xa0","")
        
        except Exception:
            price = price

    except Exception:
        pass

    item = {
        "title": title,
        "store/brand": brand,
        "price": price,
        "emi": emi.strip(),
        "description": [each.text.strip() for each in description],
        "availability": availability,
        "seller": sold_by,
        "ratings": f"{rating_stars}, total {total_raitngs}",
        "url": url
    }
    return item

if __name__ == "__main__":
    # links = get_links("laptops")
    pprint(get_details("https://www.amazon.in/HP-Pentium-Processor-15-6-inch-15s-du1052tu/dp/B08HJZHTM1/ref=sr_1_5?dchild=1&keywords=laptops&qid=1622057076&sr=8-5"))