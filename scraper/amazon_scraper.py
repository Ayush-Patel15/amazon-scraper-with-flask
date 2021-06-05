# Import statements
from urllib.parse import urljoin
from helpers import get_soup
# from concurrent.futures import ThreadPoolExecutor

AMAZON_BASE_URL = "https://www.amazon.in/s"

# function defined to extract the top 15 links for the query string from the requested page
def get_links(query,page=1):
    response = get_soup(
        AMAZON_BASE_URL,
        params=[
            ("k",query),
            ("page",page)
        ]
    )
    links = []
    tags = response.select("a.a-text-normal")
    for tag in tags:
        links.append(tag["href"])
    return links[0:15]                      # to get only the 15 urls


# function that takes a url as args and return its details
def get_details(link):
    response = get_soup(
        urljoin(AMAZON_BASE_URL, link)
    )
    try:
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
        # print(item)
    except Exception as e:
        item = {"exception": e}
    return item                      


if __name__ == "__main__":
    query,page = input("Enter your query and page number(separated by space): ").split()
    links = get_links(query,page)
    print(f"The length of link is {len(links)}")
    print(f"Top links are : {links}")
    for link in links:
        get_details(link)
    # with ThreadPoolExecutor() as executor:
    #     executor.map(get_details,links)