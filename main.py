from assets.CBGenerator import CBGenerator, HQImageScraper


if __name__ == "__main__":
    generator = CBGenerator("test", 100)
    print(generator.get_words())

    scraper = HQImageScraper()
    scraper.download_images("dog")