from assets.CBGenerator import CBGenerator, HQImageScraper
from assets.gui import GUI, ft


UI_TEST = True

if __name__ == "__main__":

    if not UI_TEST:
        generator = CBGenerator()
        generator.run(amount=10, category="spring")
        #print(generator.get_words())

        #generator.process_image()

        #HQImageScraper.download_multiple_images(words = generator.get_words())
    else:
        ft.app(target=GUI.main)

