from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import traceback
import random
import urllib.request
import undetected_chromedriver as uc

class CanvaThumb:

    def __init__(self, url):
        self.driver = None
        self.url = url
        self.sleepTime = 2
        self.thumbnails = []
        self.thumbnailsURL = []
        self.fileName = 'thumbs.txt'
        self.fileNameError = 'thumbsError.txt'
        self.countThumb = 0
        self.countSuccess = 0
        self.countError = 0

    def getWebdriver(self):
        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument("window-size=1920,1080")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument('start-maximized')
        chrome_options.add_argument('enable-automation')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-browser-side-navigation')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--log-level=3")
        dr = uc.Chrome(options=chrome_options)
        agent = dr.execute_script("return navigator.userAgent")
        print(agent)
        return dr

    def load(self):
        self.driver = self.getWebdriver()
        self.driver.get(f"{self.url}")
        time.sleep(10)
        try:
            Wait(self.driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME,  "OXyTOA")))
            print("[Carregado]: ✅")
        except:
            pass
        
        self.__acceptCookies()
        self.__getListThumbs()
        

    def __acceptCookies(self):
        try:
            print("Aceitando cookies...")
            button = self.driver.find_element(By.CLASS_NAME, "_1QoxDw")
            button.click()
            print("[Cookies]: ✅")
        except:
            pass

    def __scrollTo(self, thumb):
        try:
            print("Scrollando para objeto")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'end', behavior: 'smooth'});", thumb)
            print(f"[Scroll]: ✅")
            time.sleep(random.uniform(0.2, 0.5))
        except:
            traceback.print_exc()
            pass

    # pegar lista de thumbs
    def __getListThumbs(self):
        thumbs = self.driver.find_elements(By.CLASS_NAME, "qFtWQg")
        print(f"Total thumbs: {len(thumbs)}")
        self.thumbnails.append(thumbs)
        print(f"Thumbs Geral thumbnails: {len(self.thumbnails)}")
        countLen = self.countThumb*-1
        print(f'Count Len {countLen}')
        thumbs = thumbs[-countLen:]
        print(f"Thumbs atual: {len(thumbs)}")
        for thumb in thumbs:
            if self.countThumb % 24 == 0 and self.countThumb != 0:
                time.sleep(10)
            self.__scrollTo(thumb)
            self.__getImage(thumb)
            time.sleep(random.uniform(0.5, 1))
            self.countThumb += 1
            print(self.countThumb)
        if len(thumbs) > 0:
            time.sleep(10)
            self.__getListThumbs()
        else:
            print("Finalizado!")
            print(f"Sucesso: {self.countSuccess} ✅")
            print(f"Erro: {self.countError} ❌")

    def __getName(self, thumb):
        try:
            name = thumb.get_attribute("alt")
            print(name)
            return name
        except:
            traceback.print_exc()
            return None

    def __getImage(self, thumb):
        try:
            imageElement = thumb.find_element(By.CLASS_NAME, "AiHWyw")
            name = self.__getName(imageElement)
            nameClean = name.replace(" ", "_")
            imageURL = imageElement.get_attribute('src')
            if imageURL:
                self.countSuccess += 1
                self.thumbnailsURL.append(imageURL)
                self.__saveUrlFile(nameClean+";"+imageURL+"\n", self.fileName)
                time.sleep(0.5)
            else:
                self.countError += 1
                self.__saveUrlFile(nameClean+"\n", self.fileNameError)
                print("[NOT URL IMAGE]: ❌")
        except:
            self.countError += 1
            traceback.print_exc()
            pass

    def __saveUrlFile(self, url, file):
        print(f"[Salvando]: {url}")
        with open(file, 'a+') as f:
            f.write(url)


    # For Download all images in file thumbs.tx
    def downloadAllimages(self):
        try:
            with open(self.fileName) as f:
                lines = f.readlines()
                count = 0
                for line in lines:
                    count += 1
                    info = line.split(";")
                    if len(info) > 1:
                        name = info[0]
                        url = info[1]
                        print(f"[Baixando - {count}]: {name} - {url}")
                        self.__download_image(url, "images/", name)
                        time.sleep(random.uniform(0.4,1.2))
        except:
            traceback.print_exc()


    def __download_image(self, url, file_path, file_name):
        full_path = file_path + file_name + '.jpg'
        urllib.request.urlretrieve(url, full_path)

    
if __name__ == '__main__':
    canva = CanvaThumb("https://www.canva.com/p/bellakaweski/")
    canva.load()
    canva.downloadAllimages()