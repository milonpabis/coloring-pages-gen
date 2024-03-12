from assets.CBGenerator import CBGenerator, HQImageScraper


if __name__ == "__main__":
    generator = CBGenerator()
    generator.run("animal", 20)
    #print(generator.get_words())

    #generator.process_image()

    #HQImageScraper.download_multiple_images(words = generator.get_words())

