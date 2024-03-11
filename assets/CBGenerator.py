import random as rd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

URL = "https://relatedwords.io/"

MAIN_DIV_XPATH = "/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/span/div[1]/div[1]"

ANCHOR_XPATH = "/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/span/div[1]/div[1]/div[1]/a[1]"
ANCHOR_CLASS = "FRuiCf islib nfEiy"

IMG_CLASS = ".sFlh5c.pT0Scc.iPVvYb"

COOKIES_XPATH = "/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button/span"


class CBGenerator:

    def __init__(self, category, amount):
        self.words = WordRandomizer.generate(category, amount)
    
    def get_words(self):
        return self.words



class WordRandomizer:

    @staticmethod
    def generate(category, amount):
        response = requests.get(URL + category)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return ["Error sign"]
        result = BeautifulSoup(response.text, "html.parser")
        return [span.find("a").text for span in result.find_all("span", class_="term")[:int(amount/10)]]
    

class HQImageScraper:

    def __init__(self):
        self.url_queue = []
        self.image_urls = []
        self.driver = webdriver.Chrome()

    def get_urls(self, word):
        self.driver.get("https://www.google.com/search?q=" + word + "&tbm=isch")
        cookies = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, COOKIES_XPATH)))
        cookies.click()

        container = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, MAIN_DIV_XPATH)))
        urls = container.find_elements(By.TAG_NAME, "img")
        print("url", urls)
        cc = 0
        while not len(self.image_urls) == 10:
            url = urls[cc]
            url.click()
            try:
                img = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, IMG_CLASS)))
                if img.get_attribute("src") not in self.image_urls:
                    self.image_urls.append(img.get_attribute("src"))
            except Exception:
                pass
            cc += 2
        self.driver.quit()


        print(self.image_urls)


    def download_images(self, word):
        self.get_urls(word)

        for url in self.image_urls:
            response = requests.get(url)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                print(e)
            with open("output/" + str(rd.randint(1, 999999999999)) + ".jpg", "wb") as file:
                file.write(response.content)

        


        

