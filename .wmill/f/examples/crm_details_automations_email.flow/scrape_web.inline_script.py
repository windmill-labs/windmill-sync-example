from bs4 import BeautifulSoup
import requests
from lxml.html import html5parser
import html5lib


def main(name: str, domain: str, name_space: str):
    def search(query):
        url = "https://www.google.com/search?q={}".format(query)
        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, "lxml")
        titles = soup.find_all("h3")
        res = []
        for title in titles[:2]:
            h = html5parser.fromstring(str(title)).getchildren()[0].text
            res.append(h)
        return res

    infos = [name, domain]
    query = "+".join(map(lambda x: x.replace(" ", "+"), infos))
    try:
        res1 = search(query)
    except:
        res1 = []

    infos = [name_space, domain]
    query = "+".join(map(lambda x: x.replace(" ", "+"), infos))
    try:
        res2 = search(query)
    except:
        res2 = []

    return res1, res2
