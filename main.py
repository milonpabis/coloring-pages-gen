from assets.CBGenerator import CBGenerator, HQImageScraper


if __name__ == "__main__":
    generator = CBGenerator("food", 20)
    print(generator.get_words())

    HQImageScraper.download_multiple_images(words = generator.get_words())