from urllib.request import Request, urlopen
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

visitedPages = set()
limit = 200
count = 0

def getLinks(pageUrl):
    global visitedPages, limit, count

    # Don't remove if don't want to be IP BANed!!
    time.sleep(1)

    if limit < count:
        return

    html = requests.get(pageUrl, headers={'User-Agent': 'Mozilla/5.0'}).text
    bs = BeautifulSoup(html, 'html.parser')
    print(pageUrl)

    for link in bs.find_all('a'):
        if 'href' in link.attrs and pageUrl[:-1] in urljoin(pageUrl, link.attrs['href']) and "#" not in urljoin(pageUrl, link.attrs['href']):
            newPage = urljoin(pageUrl, link.attrs['href'])

            if newPage not in visitedPages:
                visitedPages.add(newPage)
                count += 1
                getLinks(newPage)

def main():
    getLinks(input("Input URL: "))
    f = open('url_list.txt', 'w', encoding='UTF-8')
    f.writelines(list(visitedPages))
    f.close()

if __name__ == "__main__":
    main()
