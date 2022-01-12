import requests
import sys
from bs4 import BeautifulSoup
import json

def _num_to_int(num):
    """
    get a number in human readable form to int (e.g. "110 100" -> 110100)
    """

    if num.lower() == "free": return 0
    
    return int(num.replace(" ", ""))

def _get_currency(value):

    currencies = {
        "/images/thumb/5/56/Specs-Card-Activity.png/23px-Specs-Card-Activity.png" : "squadron_points",
        "/images/thumb/4/4f/Specs-Card-Exp.png/14px-Specs-Card-Exp.png" : "research_points",
        "/images/c/c1/Specs-Card-Lion.png" : "silver_lions",
        "/images/f/f6/Specs-Card-Eagle.png" : "golden_eagles",
    }

    try:
        return currencies[value.find("a").find("img")["src"]]
    except:
        return None


def _get_price(soup):
    """
    get the currency from a price tag (research or buy)
    """

    pricetag = soup.find("div", {"class" : "general_info_price"})

    research_currency = None
    research_price = None
    buy_currency = None
    buy_price = None

    buy_info = pricetag.find("div", {"class" : "general_info_price_buy"})
    buy_price_text = buy_info.find("span", {"class", "value"}).text

    # if it's a gift vehicle return 
    if buy_price_text == "Bundle or Gift":
        buy_currency = "bundle_gift"
    else:
        buy_price = _num_to_int(buy_price_text)
        buy_currency = _get_currency(buy_info)

        if research_info := pricetag.find("div", {"class" : "general_info_price_research"}):
            research_price = _num_to_int(research_info.find("span", {"class" : "value"}).text)
            research_currency = _get_currency(research_info)

    return {
        "research_currency" : research_currency,
        "research_price": research_price,
        "buy_currency": buy_currency,
        "buy_price": buy_price
    }

def _get_economy(soup):
    """
    get the economy costs of a vehicle
    """
    
    economy = {
        "repair_AB_spaded": None,
        "repair_RB_spaded": None,
        "repair_SB_spaded": None,
        "repair_AB_base": None,
        "repair_RB_base": None,
        "repair_SB_base": None,
        "modifications_cost_rp": None,
        "modifications_cost_sl": None,
        "crew_cost_training": None,
        "crew_cost_expert": None,
        "crew_cost_ace_ge": None,
        "crew_cost_ace_rp": None,
    }

    economy_head = soup.find("h3", text="Modifications and economy")
    economy_table = economy_head.find_next_sibling()

    # get the repair costs
    for mode in ["AB", "RB", "SB"]:
        repairs_cost = economy_table.find("span", text=mode).find_next_sibling().text.split("→")
        
        economy["repair_%s_spaded" % mode] = _num_to_int(repairs_cost[-1])

        # try to get the base repair cost (not available for premium vehicles)
        try:
            economy["repair_%s_base" % mode] = _num_to_int(repairs_cost[-2])
        except:
            pass

    # modifications cost (not available on premium vehicles)
    try:
        modifications_head = economy_table.find("span", text="Total cost of modifications")
        economy["modifications_cost_rp"] = _num_to_int(modifications_head.find_next_sibling().text)
        economy["modifications_cost_sl"] = _num_to_int(modifications_head.find_parent().find_next_sibling().find("span", {"class" : "value"}).text)
    except:
        pass

    # get the crew costs
    economy["crew_cost_training"] = _num_to_int(economy_table.find("span", text="Crew training").find_next_sibling().text)
    economy["crew_cost_expert"] = _num_to_int(economy_table.find("span", text="Experts").find_next_sibling().text)
    economy["crew_cost_ace_ge"] = _num_to_int(economy_table.find("span", text="Aces").find_next_sibling().text)
    economy["crew_cost_ace_rp"] = _num_to_int(economy_table.find("span", text="Research Aces").find_next_sibling().text)

    return economy


def _parse_page(page):
    soup = BeautifulSoup(page, "html.parser")

    name = soup.find("div", {"class" : "general_info_name"}).text.strip()
    name_no_symbols = soup.find("h1", {"id" : "firstHeading"}).text.strip()
    nation = soup.find("div", {"class" : "general_info_nation"}).text.strip()
    rank_text = soup.find("div", {"class" : "general_info_rank"}).text.strip()
    rank = rank_text.split(" ")[0]

    brs = soup.find("div", {"class" : "general_info_br"}).find_all("td")[3:]
    br_AB = float(brs[0].text.strip())
    br_RB = float(brs[1].text.strip())
    br_SB = float(brs[2].text.strip())

    classes = [c.text.lower() for c in soup.find("div", {"class" : "general_info_class"}).find_all("a")]

    if "premium" in classes: type = "premium"
    elif "squadron" in classes: type = "squadron"
    else: type = "techtree"

    buy_info = _get_price(soup)

    repair_info = _get_economy(soup)
        
    return {
        "name": name,
        "name_no_symbols": name_no_symbols,
        "nation": nation,
        "rank_text": rank_text,
        "rank": rank,
        "br_AB": br_AB,
        "br_RB": br_RB,
        "br_SB": br_SB,
        "classes": classes,
        "type": type,
        "buy_info": buy_info,
        "economy_info": repair_info,
    }

def get_vehicle_info(url):
    """
    get the vehicle info from a wiki page (e.g. https://wiki.warthunder.com/MiG-19S_(Germany))
    """
    page = requests.get(url).text
    return _parse_page(page)

def main():
    if len(sys.argv) < 2:
        print("Usage: python get_vehicle_info.py <vehicle_wiki_url>")
        sys.exit(1)

    url = sys.argv[1]

    info = get_vehicle_info(url)

    print(json.dumps(info, indent=4))

if __name__ == "__main__":
    main()