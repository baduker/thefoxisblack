#!/usr/bin/python

import os
import requests


from bs4 import BeautifulSoup as bs


MAX_PAGES = 1
SAVE_DIR = 'fox_backgrounds'
BASE_URL = "http://www.thefoxisblack.com/category/the-desktop-wallpaper-project/page/%s/"
RESOLUTIONS = [
            "1280x800", "1440x900", "1680x1050", "1920x1200", "2560x1440",
            "iphone", "iphone-5", "iphone6", "iphone-6-plus", "iphone6plus",
            "ipad",
            ]

LOGO = """
  __            _       _     _            _    
 / _| the      (_)     | |   | |          | |   
| |_ _____  __  _ ___  | |__ | | __ _  ___| | __
|  _/ _ \ \/ / | / __| | '_ \| |/ _` |/ __| |/ /
| || (_) >  <  | \__ \ | |_) | | (_| | (__|   < 
|_| \___/_/\_\ |_|___/ |_.__/|_|\__,_|\___|_|\_\\
                                                
                        a simple image downloader
"""


def show_logo():
    print(LOGO)


def fetchurl(url):
    return requests.get(url).text


def get_images_from_page(url):
    html = fetchurl(url)
    soup = bs(html, "html.parser")
    for link in soup.find_all("a", class_="btn_download"):
        href = link["href"]
        for res in RESOLUTIONS:
            if res in href:
                print("Downloading: {}".format(href))
                r = requests.get(href)
                with open("fox_backgrounds%s" % href[href.rfind('/'):], 'wb') as f:
                        f.write(r.content)


def get_backgrounds():
    show_logo()
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    for x in range(0, MAX_PAGES):
        get_images_from_page(BASE_URL % (x + 1))


if __name__ == '__main__':
    get_backgrounds()
