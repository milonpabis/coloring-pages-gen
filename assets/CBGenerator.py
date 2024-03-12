import random as rd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import threading
import datetime as dt
import cv2 as cv
import numpy as np
import shutil
import os
from time import sleep


URL = "https://relatedwords.io/"
MAIN_DIV_XPATH = "/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/span/div[1]/div[1]"
IMG_CLASS = ".sFlh5c.pT0Scc.iPVvYb"
COOKIES_XPATH = "/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button/span"
COOKIES_XPATH2 = "/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button/div[3]"


class CBGenerator:

    def __init__(self, path: str = "output/") -> None:
        self.__path = path

    
    def run(self, amount: int = 20, category: str = "music", method: int = 3, words: list[str] = None, preview: bool = False) -> None:
        if not words:
            words = WordRandomizer.generate(category, int(amount/10))
        os.makedirs(self.__path, exist_ok=True)
        os.makedirs(self.__path + "ready/", exist_ok=True)
        HQImageScraper.download_multiple_images(words, self.__path)
        for image in os.listdir(self.__path):
            if image.endswith(".jpg") and image:
                self.process_image(self.__path + image, method=method, preview=preview)
            else: print("SKIPPED:", image)

    
    def get_path(self) -> str:
        return self.__path
    

    def process_image(self, url: str, basename: str = "res", method: int = 1, preview: bool = False) -> None:
        """
        Processes the image by drawing its contours on white plane and saves it to the output directory.

        Parameters: 
            url (str): Local URL of the image to be processed.
            preview (bool): Gate for the preview of the processed image.
            method (int): The method of processing the image. 1 - Contours with adaptive thresholding, 2 - Canny edge detection, 3 - Adaptive Canny edge detection.

        Returns: 
            None
        """
        image = cv.imread(url)
        try:
            gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        except Exception:
            print(url, "ERROR")
            return
        if method == 1:
            result = np.ones((image.shape[0], image.shape[1], 3), dtype=np.uint8) * 255
            thr1 = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 13, 2)
            contours, _ = cv.findContours(thr1, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            cv.drawContours(result, contours, -1, (0, 0, 0), 1)

        elif method == 2:
            edges = cv.Canny(gray,100,120, apertureSize=3, L2gradient=False)
            result = cv.bitwise_not(edges)
        
        elif method == 3:
            ret, _ = cv.threshold(gray, thresh=0, maxval=255, type=(cv.THRESH_BINARY + cv.THRESH_OTSU))
            edges = cv.Canny(gray, threshold1=(ret * 0.4), threshold2=ret)
            result = cv.bitwise_not(edges)

        if preview:
            cv.imshow("image", image)
            cv.imshow("result", result)
            cv.waitKey(0)
            cv.destroyAllWindows()
        
        cv.imwrite(f"{self.__path}ready/" + f"{basename}{rd.randint(1, 9999999999)}.jpg", result)



class WordRandomizer:

    @staticmethod
    def generate(category: str, amount: int) -> list[str]:
        """
        Returns the list of random words associated with given category.

        Parameters: 
            category (str): The category representing the words.
            amount (int): The amount of words to be generated.

        Returns: 
            (list)[str]: The list containing the words. In case of an error, the list containing the string "Error sign" is returned.
        """
        response = requests.get(URL + category)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return ["Error sign"]
        result = BeautifulSoup(response.text, "html.parser")
        return [span.find("a").text for span in result.find_all("span", class_="term")[:amount]]
    

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
        try:
            cookies = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, COOKIES_XPATH)))
            cookies.click()
        except Exception as e:
            print("COOKIES:", e)
            try:
                cookies = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, COOKIES_XPATH2)))
                cookies.click()
            except Exception as e:
                print("COOKIES:", e)
                try:
                    cookies = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Zaakceptuj wszystko')]")))
                    cookies.click()
                except Exception as e:
                    print("COOKIES:", e)
                    sleep(30)


        container = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, MAIN_DIV_XPATH)))
        urls = container.find_elements(By.TAG_NAME, "img")
        #print("url", urls)
        cc = 0
        while not len(word_urls) == 10:
            url = urls[cc]
            try:
                if url.get_attribute("data-sz") != "16":
                    raise Exception
            except Exception:
                try:
                    url.click()
                    try:
                        img = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, IMG_CLASS)))
                        if img.get_attribute("src") not in word_urls and img.get_attribute("src") != None:
                            if not img.get_attribute("src").endswith(".gif"):
                                word_urls.append(img.get_attribute("src"))
                    except Exception:
                        pass
                except Exception:
                    pass
            cc += 1

        driver.quit()

        return word_urls


    def download_images(word: str, path: str) -> None:
        """
        Downloads the images representing the word.

        Parameters: 
            word (str): The word representing an object on the images.
            path (str): The path to the directory where the images will be saved.

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
                    print("DOWNLOAD ERROR:", e)
                with open(path + str(rd.randint(1, 999999999999)) + ".jpg", "wb") as file:
                    file.write(response.content)
            except Exception:
                pass


    def download_multiple_images(words: list[str], path: str) -> None:
        """
        Downloads the images representing the words.

        Parameters: 
            words (list)[str]: The list containing the words representing an object on the images.
            path (str): The path to the directory where the images will be saved.

        Returns: 
            None 
        """
        MULTI = False
        start = dt.datetime.now()

        if MULTI:

            threads = []

            for word in words:
                thread = threading.Thread(target=HQImageScraper.download_images, args=(word,path,))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()
        else:
            for word in words:
                HQImageScraper.download_images(word, path)

        print("All images downloaded. TIME:", dt.datetime.now() - start)

# TODO:
        # 1. When skips a lot of images -> clicks a link - block it
        # 2. Multithreading upgrade - concurret.futures
        # 3. Cookies problem - fix it, make it universal




        


        

