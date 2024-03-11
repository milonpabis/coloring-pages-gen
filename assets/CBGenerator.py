import random as rd
import requests
from bs4 import BeautifulSoup

URL = "https://relatedwords.io/"

MAIN_DIV = "/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/span/div[1]/div[1]"


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

    def get_urls(self, word):
        response = requests.get("https://www.google.com/search?q=" + word + "&tbm=isch")
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print("Error - url Scraper")
            return
        result = BeautifulSoup(response.text, "html.parser")
        self.url_queue = [a["href"] for a in result.find_all("a") if a["href"].startswith("https://www.google.com/imgres?")]
        print(self.url_queue)

        


        

