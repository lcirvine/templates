import requests
from bs4 import BeautifulSoup


def return_soup(url: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', }
    with requests.get(url, headers=headers, verify=False) as r:
        soup = BeautifulSoup(r.text, 'html.parser')
    return soup

