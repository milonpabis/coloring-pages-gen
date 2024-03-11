import random as rd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import threading
import datetime as dt


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


    def get_urls(word: str) -> list[str]:
        """
        Returns the list containing the urls of the images representing the word.

        Parameters: 
            word (str): The word representing an object on the images.

        Returns: 
            (list)[str]: The list containing the urls of the images representing the word. 
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.headless = False
        driver = webdriver.Chrome(options=chrome_options)
        word_urls = []
        driver.get("https://www.google.com/search?q=" + word + "&tbm=isch")
        cookies = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, COOKIES_XPATH)))
        cookies.click()

        container = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, MAIN_DIV_XPATH)))
        urls = container.find_elements(By.TAG_NAME, "img")
        print("url", urls)
        cc = 0
        urlurl = []
        while not len(word_urls) == 10:
            url = urls[cc]
            try:
                #urlurl.append(url["src"])
                url.click()
                try:
                    img = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, IMG_CLASS)))
                    if img.get_attribute("src") not in word_urls:
                        word_urls.append(img.get_attribute("src"))
                except Exception:
                    pass
            except Exception:
                pass
            cc += 1

        driver.quit()

        with open("output/urls.txt", "a") as f:
            for url in urlurl:
                f.write(url + "\n")


        return word_urls


    def download_images(word: str) -> None:
        """
        Downloads the images representing the word.

        Parameters: 
            word (str): The word representing an object on the images.

        Returns: 
            None 
        """

        urls = HQImageScraper.get_urls(word)

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        for url in urls:
            try:
                response = requests.get(url, headers=headers)
                try:
                    response.raise_for_status()
                except requests.exceptions.HTTPError as e:
                    print(e)
                with open("output/" + str(rd.randint(1, 999999999999)) + ".jpg", "wb") as file:
                    file.write(response.content)
            except Exception:
                pass


    def download_multiple_images(words: list[str]) -> None:
        """
        Downloads the images representing the words.

        Parameters: 
            words (list)[str]: The list containing the words representing an object on the images.

        Returns: 
            None 
        """
        MULTI = True
        start = dt.datetime.now()

        if MULTI:

            threads = []

            for word in words:
                thread = threading.Thread(target=HQImageScraper.download_images, args=(word,))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()
        else:
            for word in words:
                HQImageScraper.download_images(word)

        print("All images downloaded. TIME:", dt.datetime.now() - start)


        


        

