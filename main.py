from wallpaper import get_wallpaper, set_wallpaper
from bs4 import BeautifulSoup as bs
import requests
from datetime import datetime as date
import os
import hashlib

def file_as_bytes(file_path):
    with open(file_path,'rb') as f:
        return f.read()

def getImage():
    base_url = requests.get("https://www.bing.com")
    res = bs(base_url.content,"html.parser")
    x = res.find("li",class_="item download")
    img_url = base_url.url[:-1] + x.next_element['href']
    img = requests.get(img_url).content
    now = date.now().strftime(r"%Y%m%d")
    ext = img_url.split(".")[-1]
    img_path = f"data/bingWallpaper_{now}.{ext}"
    return img,img_path,now,ext

def isHashSame(img,img_path):
    new_img_hash = hashlib.blake2s(img).hexdigest()
    old_img_hash = hashlib.blake2s(file_as_bytes(img_path)).hexdigest()
    if new_img_hash == old_img_hash:
        return True
    return False

def isImagePresent(img,img_path,now,ext):
    if os.path.exists(img_path):
        if isHashSame(img,img_path):
            return True,img_path
        else:
            index = 1
            img_path = "data/bingWallpaper_{}_{}.{}"
            new_path = img_path.format(now,index,ext)
            while os.path.exists(new_path):
                if isHashSame(img,new_path):
                    return True,new_path
                index+=1
                new_path = img_path.format(now,index,ext)
            return False,new_path
    else:
        return False,img_path

def changeWall():
    try:
        print("Project Bing Initiated !!")
        if not os.path.exists("data"):
            print("Creating image repository folder: ./data")
            os.makedirs("data")
        
        img,img_path,now,ext = getImage()
        cond,img_path = isImagePresent(img,img_path,now,ext)
        if cond:
            print("Image already present",img_path)
            present_wall = get_wallpaper()
            isEqual = os.path.basename(present_wall) == os.path.basename(img_path)
            if isEqual:
                print("Wallpaper already applied")
                return
            else:
                print("Applying wallpaper")
                set_wallpaper(img_path)
                return
        else:
            print("Saving Image",os.path.basename(img_path))
            with open(img_path,"wb") as f:
                f.write(img)
        print("Applying latest wallpaper")
        set_wallpaper(img_path)
        print("Project Bingo Successfully completed!!")
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("Connection Error")
        print("Project Bing Failed!!")

changeWall()