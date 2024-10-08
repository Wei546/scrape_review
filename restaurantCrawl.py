import json
from ssl import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class ScrapeInfo():
    # 建構子
    def __init__(self, url):
        self.url = url
        self.option = Options()
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.option)
        self.driver.get(url)
        self.wait = WebDriverWait(self.driver, 20)
        self.totalRev = "div div.fontBodySmall"
        self.username = ".d4r55"
        self.reviews = ".MyEned"
        self.totalRevCount = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, self.totalRev))).get_attribute("textContent").split(' ')[0].replace(',','').replace('.','')
        self.mydict = {}
        self.found = 0
        self.info_btn = ".hh2c6"
        self.restaurant_name_class=".tAiQdd h1.DUwDvf"
        # Extract address, website, phone, and appointment link
        self.restaurant_detail_class=".CsEnBe"
    # 點擊展開按鈕
    def click_expand_buttons(self):
        try:
            expand = ".w8nwRe.kyuRq" 
            expand_buttons = self.driver.find_elements(By.CSS_SELECTOR, expand) 
            for button in expand_buttons:
                if button.is_displayed():  
                    self.driver.execute_script("arguments[0].scrollIntoView();", button) 
                    button.click() 
                    time.sleep(1)
        except Exception as e:
            print("Error in click_expand_buttons: ", e)

    # 爬取評論
    def scrape_reviews(self):
        while self.found < int(self.totalRevCount):
            review_elements = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.reviews)))
            reviewer_names = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.username)))
            self.found = len(self.mydict)
            for rev, name in zip(review_elements, reviewer_names):
                self.click_expand_buttons()
                print("rev - ", rev.text)
                if name.text not in self.mydict:      
                    self.mydict[name.text] = rev.text
                if len(rev.text) == 0:
                    self.found = int(self.totalRevCount) + 1 
                    break
            for i in range(3):
                ActionChains(self.driver).key_down(Keys.ARROW_DOWN).perform()
            time.sleep(1)
            if len(reviewer_names) >= int(self.totalRevCount):
                print(f"Collected all reviews. Breaking the loop. Found: {self.found}, Total Reviews: {self.totalRevCount}")
                break
            with open('reviews.json', 'w',encoding="utf8",newline="") as f:
                json.dump(self.mydict, f, ensure_ascii=False, indent=4)
            self.driver.quit()
if __name__ == "__main__":
    url = "https://www.google.com/maps/place/OK%E4%BE%BF%E5%88%A9%E5%95%86%E5%BA%97%EF%BC%88%E8%99%8E%E5%B0%BE%E5%BE%B7%E8%88%88%E5%BA%97%EF%BC%89/@23.6947809,120.4139397,14z/data=!4m12!1m2!2m1!1z6JmO5bC-T0s!3m8!1s0x346eb1be55c5b691:0xd6f20c5f53411911!8m2!3d23.7090285!4d120.4316976!9m1!1b1!15sCgjomY7lsL5PS1oLIgnomY7lsL4gb2uSARFjb252ZW5pZW5jZV9zdG9yZeABAA!16s%2Fg%2F11pcp9qf1h?entry=ttu&g_ep=EgoyMDI0MTAwMi4xIKXMDSoASAFQAw%3D%3D"
    scrape = ScrapeInfo(url)
    scrape.scrape_reviews()
