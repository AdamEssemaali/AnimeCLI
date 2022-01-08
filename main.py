import bs4
import requests
from urllib.parse import urljoin
import subprocess
baseURL = "https://www.animeworld.tv"

class AnimeRAW:
    def __init__(self, href, name) -> None:
        self.href = href
        self.name = name


def findAnime(name):
    animes = []
    
    req = requests.get("https://www.animeworld.tv/search?keyword=" + str(name).replace(" ", "%20"))
    soup = bs4.BeautifulSoup(req.text, "html.parser")
    for anime in soup.find_all("div", {"class": "item"}):
        animes.append(AnimeRAW(anime.find("a")["href"], anime.find("img").get("alt")))
    return animes



def playAnime(anime):
    req = requests.get(anime)
    launch = None
    soup = bs4.BeautifulSoup(req.text, "html.parser")
    for link in soup.find_all("a", {"id": "downloadLink"}):
        launch = link.get("href")
    reql = requests.get(launch)
    soupL = bs4.BeautifulSoup(reql.text, "html.parser")
    for link in soupL.find_all("a", {"class": "btn btn-primary p-2"}):
        # get the current url
        url = urljoin(launch, link.get("href"))
        subprocess.call(["mpv", url])
    return None


def getAllEpisodes(anime):
    req = requests.get(baseURL + anime.href)
    soup = bs4.BeautifulSoup(req.text, "html.parser")
    episodes = []
    for ep in soup.find_all("li", {"class": "episode"}):
        episodes.append(ep.find("a")["href"])
    print(episodes)
    return episodes
counter = 0
animes = findAnime("boku")
for anim in animes:
    print(f"[{counter}] {anim.name}")
    counter += 1

getter = animes[int(input("> "))]
episodes = getAllEpisodes(getter)
counter = 0
for ep in episodes:
    print(f"[{counter}] EPISODE {counter +1}")
    counter += 1

playAnime(urljoin(baseURL,episodes[int(input("> "))]))
