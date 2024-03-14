from assets.CBGenerator import CBGenerator, HQImageScraper
from assets.gui import GUI, ft


UI_TEST = True

if __name__ == "__main__":

    if not UI_TEST:
        generator = CBGenerator("F:/Desktop/")
        generator.run(amount=20, category="water")
        #print(generator.get_words())

        #generator.process_image()

        #HQImageScraper.download_multiple_images(words = generator.get_words())
    else:
        window = GUI()
        ft.app(target=window.main)


# TODO:
        # 1. When skips a lot of images -> clicks a link - block it 
        # 2. Add a bufforing circle for the image download
        # 3. naming for words -> directory

        

