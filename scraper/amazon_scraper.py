# Import statements
from urllib.parse import urljoin
from pprint import pprint
from helpers import get_soup, limiting_ouptut


AMAZON_BASE_URL = "https://www.amazon.in/s"


# function defined to extract all the available links for the query string
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


# functions that takes a list of urls as args and return its details
def get_details(links,page):
    product_details = []
    offset,limit = limiting_ouptut(page)
    for link in links[offset:limit]:
        response = get_soup(
            urljoin(AMAZON_BASE_URL, link)
        )

        # common attributes present for all queries
        details_section = response.select('#centerCol')[0]
        url = urljoin(AMAZON_BASE_URL,link)
        title = details_section.select('#productTitle')[0].text.strip()
        brand = details_section.select('#bylineInfo')[0].text
        description = details_section.select('#feature-bullets')[0].select(".a-list-item")

        # get the normal price or the special deal price
        if details_section.select('#priceblock_ourprice'):
            price = details_section.select('#priceblock_ourprice')[0].text.replace("\xa0","")
        elif details_section.select('#priceblock_dealprice'):
            price = details_section.select('#priceblock_dealprice')[0].text.replace("\xa0","")
        else:
            price = 'NA'

        # try and except blocks:-> try to extract individual attribute or return NA"
        try:
            availability = details_section.select("#availability")[0].text.strip()
        except Exception:
            availability = "not in stock"
        try:
            sold_by = details_section.select("#sellerProfileTriggerId")[0].text
        except Exception:
            sold_by = "NA"
        try:
            emi = details_section.select("#inemi_feature_div")[0].select("span")[0].text
        except Exception:
            emi = "not available"
        try:   
            rating_stars = details_section.select("#acrPopover")[0]["title"]
            total_raitngs = details_section.select("#acrCustomerReviewText")[0].text
        except Exception:
            rating_stars = "0.0 out of 5 stars"
            total_raitngs = "0"

        item = {
            "title": title,
            "store/brand": brand,
            "price": price,
            "emi": emi.strip(),
            "description": [each.text.strip() for each in description],
            "availability": availability,
            "seller": sold_by,
            "ratings": f"{rating_stars}, ratings {total_raitngs}",
            "url": url
        }
        product_details.append(item)
    return product_details                      # returns a list


if __name__ == "__main__":
    links = get_links("laptops")
    pprint(get_details(links))