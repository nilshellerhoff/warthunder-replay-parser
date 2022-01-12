import requests
import sys
from bs4 import BeautifulSoup
import json

def _parse_page(page):
    soup = BeautifulSoup(page, "html.parser")

    vehicle_tags = soup.find_all("div", {"class": "tree-item"})

    vehicles = []
    for vehicle in vehicle_tags:
        image = vehicle.find("div", {"class": "tree-item-img"}).find("img")["src"]
        slug = image.split('/')[-1].split('.')[0]
        name = vehicle.find("span", {"class": "tree-item-text-scroll"}).text
        link = vehicle.find("a")["href"]

        vehicles.append({
            "slug": slug,
            "name": name,
            "link": link,
            "image": image
        })

    return vehicles

def get_vehicles(url):
    """
    get all the vehicles listed on a wiki page (e.g. https://wiki.warthunder.com/Category:Germany_aircraft))
    """
    page = requests.get(url).text
    return _parse_page(page)


def main():
    if len(sys.argv) < 2:
        print("Usage: python aircraft_wiki.py <aircraft_wiki_url>")
        sys.exit(1)

    url = sys.argv[1]

    vehicles = get_vehicles(url)

    print(json.dumps(vehicles, indent=4))

if __name__ == "__main__":
    main()