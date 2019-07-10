#!/usr/bin/python3

import os
import requests


from bs4 import BeautifulSoup as bs
from pathlib import Path
from shutil import copyfileobj


LOGO = """
  __            _       _     _            _    
 / _| the      (_)     | |   | |          | |   
| |_ _____  __  _ ___  | |__ | | __ _  ___| | __
|  _/ _ \ \/ / | / __| | '_ \| |/ _` |/ __| |/ /
| || (_) >  <  | \__ \ | |_) | | (_| | (__|   < 
|_| \___/_/\_\ |_|___/ |_.__/|_|\__,_|\___|_|\_\\
                                                
                        a simple image downloader
"""


MAX_PAGES = 1  # Max. number of pages is 41
SAVE_DIRECTORY = Path('fox_backgrounds')
BASE_URL = 'http://www.thefoxisblack.com/category/the-desktop-wallpaper-project/page'
RESOLUTIONS = {
    '1280x800', '1440x900', '1680x1050', '1920x1200', '2560x1440',
    'iphone', 'iphone-5', 'iphone6', 'iphone-6-plus', 'iphone6plus',
    'ipad'
    }


def show_logo():
    print(LOGO)


def fetch_url(url):
    return requests.get(url).text


def clip_part(href):
    return href.rpartition('/')[-1]


def save_image(href):
    part = clip_part(href)
    print(f'Downloading: {part}')
    fn = SAVE_DIRECTORY / part
    with requests.get(href, stream=True) as response, \
        open(fn, 'wb') as output:
        copyfileobj(response.raw, output)


def get_images_from_page(url):
    html = fetch_url(url)
    soup = bs(html, 'html.parser')
    for link in soup.find_all('a', class_='btn_download'):
        href = link['href']
        if any(href.endswith(f'-{res}.jpg') for res in RESOLUTIONS):
            save_image(href)
        else:
            print(f'Unknown resolution {href}')


def make_dir():
    os.makedirs(SAVE_DIRECTORY, exist_ok=True)


def get_backgrounds():
    show_logo()
    make_dir()
    for page in range(1, MAX_PAGES+1):
        print(f'Fetching page {page}...')
        get_images_from_page(f'{BASE_URL}{page}')


def main():
    get_backgrounds()


if __name__ == '__main__':
    main()
