from wallpaper import get_wallpaper, set_wallpaper
from bs4 import BeautifulSoup as bs
import requests
from datetime import datetime as date
import os

def changeWall():
    try:
        print("Project Bing Initiated!!")
        if not os.path.exists("data"):
            os.makedirs("data")
        base_url = requests.get("https://www.bing.com")
        res = bs(base_url.content,"html.parser")
        x = res.find("li",class_="item download")
        img_url = base_url.url[:-1] + x.next_element['href']
        r = requests.get(img_url)
        now = date.now().strftime(r"%Y%m%d")
        ext = img_url.split(".")[-1]
        img_path = f"data/bingWallpaper_{now}.{ext}"
        if os.path.exists(img_path):
            print("Wallpaper already present")
            present_wall = get_wallpaper()
            isEqual = os.path.basename(present_wall) == os.path.basename(img_path)
            print(get_wallpaper(),isEqual)
            if isEqual:
                print("Wallpaper already applied")
                return
        else:
            print(f"Saving new wallpaper: {os.path.basename(img_path)}")
            with open(img_path,"wb") as f:
                f.write(r.content)
        set_wallpaper(img_path)
        print("Project Bing Successful!!")
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("Connection Error")
        print("Project Bing Failed!!")

changeWall()