# import statements 
from helpers import get_soup
import random

BEST_DEALS_URL = "https://www.amazon.in/"

# This function will return the best deals of the day as per amazon
def deals_of_the_day():
    links_tag = []
    deals_link = []
    images_link = []
    try:
        response = get_soup(BEST_DEALS_URL)
        deals_section = response.select(".product-shoveler")
        for deals in deals_section:
            links_tag.append(deals.select("a"))
        links = random.choice(links_tag)
        # slicing is to remove unwanted hrefs
        for link in links[:-2]:
            deals_link.append(link["href"])
            images_link.append(link.select("img")[0]["src"])
        items = list(zip(deals_link,images_link))
        return items
    except Exception:
        pass

def main_deals():
    result = deals_of_the_day()
    if result == None:
        try:
            deals = deals_of_the_day()
        except Exception:
            deals = [("no data","no image"),("no data","no image"),("no data","no image"),("no data","no image"),("no data","no image"),("no data","no image"),("no data","no image")]
    else:
        deals = result
    return deals

if __name__ == "__main__":
    deals = main_deals()
    print(deals)
    # print(len(deals))
