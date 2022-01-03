import requests
import json
from bs4 import BeautifulSoup as bs
import sys

def fetch_page(url, cookies):
    """
    fetch the source of a page
    """
    r = requests.post(url, cookies=cookies)
    return r.text

def parse_page(page):
    """
    parse a html replay page and return all the replays on it
    """
    return_replays = []

    soup = bs(page, 'html.parser')
    replays = soup.find_all('a', class_='replay__item')

    for r in replays:
        id = r['data-replay']
        title = r.find('div', class_="replay__title").contents[0]
        date = r.find('span', class_='date__text').contents[0]
        duration = r.find('div', class_='stat-column').find('span', class_='text-left').contents[0]

        col6 = r.find_all('div', class_='col-6')
        (gametype, mission, vehicles, gamemode) = ("","","","")
        for c in col6:
            soup = bs(str(c), 'html.parser')
            if soup.find("span", class_="stat__label").contents[0] == "Game type:":
                gametype = soup.find("span", class_="stat__value").contents[0]
            if soup.find("span", class_="stat__label").contents[0] == "Mission:":
                mission = soup.find("span", class_="stat__value").contents[0]
            if soup.find("span", class_="stat__label").contents[0] == "Vehicles:":
                vehicles = soup.find("span", class_="stat__value").contents[0]
            if soup.find("span", class_="stat__label").contents[0] == "Game mode:":
                gamemode = soup.find("span", class_="stat__value").contents[0]        

        return_replays.append({
            "id": id,
            "title": title,
            "date": date,
            "duration": duration,
            "gametype": gametype,
            "mission": mission,
            "vehicles": vehicles,
            "gamemode": gamemode
        })

    return return_replays

def download_pages(num_pages, cookies):
    """
    download the replay list from warthunder.com
    """

    # construct the urls (first page must not have page index)
    urls = ["https://warthunder.com/en/tournament/replay/"]
    if num_pages > 1:
        urls += ["https://warthunder.com/en/tournament/replay/page/{}?Filter=&action=search".format(i) for i in range(2, num_pages+1)]

    pages = []
    for url in urls:
        pages.append(fetch_page(url, cookies))
    
    return pages

def main():
    try: 
        num_pages = int(sys.argv[1])
    except:
        num_pages = 1

    # load the auth cookie
    with open("auth_cookie.json") as f:
        cookies = json.load(f)

    pages = download_pages(num_pages, cookies)

    replays = []
    for page in pages:
        replays += parse_page(page)
        
    print(json.dumps(replays, indent=4))

if __name__ == "__main__":
    main()