from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import json
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
import sys
import time

# adding path to geckodriver to the OS environment variable
os.environ["PATH"] += os.pathsep + os.getcwd()
download_path = "dataset/"


def main():
    print("\n********* Image Crawler by DHINESH KUMAR M *********\n")

    query_ = input("Enter Query: ").title()
    searchtext = query_.replace(" ","+")
    num_requested = int(input("No of Images: "))
    print(query_)
    number_of_scroll = int(num_requested / 400 + 23)
    print("Number of Scroll: {}".format(number_of_scroll))
    # number_of_scrolls * 400 images will be opened in the browser

    if not os.path.exists(download_path + query_):
        os.makedirs(download_path + query_)

    url = "https://www.google.co.in/search?q=" + searchtext + "&source=lnms&tbm=isch"
    #url = "https://www.google.com/search?q="+searchtext+"+site:shutterstock.com&client=firefox-b-ab&source=lnms&tbm=isch&sa=X&ved=0ahUKEwj21O2SgrnYAhUmI8AKHfUOCboQ_AUICigB&biw=1366&bih=674"
    driver = webdriver.Firefox()
    driver.get(url)

    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
    extensions = {"jpg", "jpeg", "png"}
    img_count = 0
    downloaded_img_count = 0

    for _ in range(number_of_scroll):
        for __ in range(10):
            # multiple scrolls needed to show all 400 images
            driver.execute_script("window.scrollBy(0, 1000000)")
            time.sleep(0.2)
        # to load next 400 images
        time.sleep(0.5)
        try:
            driver.find_element_by_xpath("//input[@value='Show more results']").click()
        except Exception as e:
            print ("Less images found:", e)
            break
            
    imges = driver.find_elements_by_xpath('//div[contains(@class,"rg_meta")]')
    print("Total images:", len(imges), "\n")
    for img in imges:
        img_count += 1
        img_url = json.loads(img.get_attribute('innerHTML'))["ou"]
        img_type = json.loads(img.get_attribute('innerHTML'))["ity"]
        print("Downloading image", img_count, ": ", img_url)
        try:
            if img_type not in extensions:
                img_type = "jpg"
            req = Request(img_url, headers=headers)
            raw_img = urlopen(req).read()
            f = open(download_path + query_+ "/" + str(downloaded_img_count) + "." + img_type,
                     "wb")
            f.write(raw_img)
            f.close
            downloaded_img_count += 1
        except Exception as e:
            print("Download failed:", e)
        finally:
            print
        if downloaded_img_count >= num_requested:
            break

    print("Total downloaded: ", downloaded_img_count, "/", img_count)
    driver.quit()


if __name__ == "__main__":
    main()
