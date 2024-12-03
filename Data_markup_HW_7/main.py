import driver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import json

options = Options()
options.add_argument('start-maximized')

driver = webdriver.Chrome(options=options)

driver.get('https://book24.ru/catalog/detskaya-poeziya-1162/?author_id=132356')

#driver.get('https://book24.ru/')
time.sleep(4)
#close_window=driver.find_element(By.XPATH, "//div/button[@class = 'location-d__popup-close']").click()
# input = driver.find_element(By.XPATH, "//div/input[@value class ='b24-input-control__input']")
# input.send_keys('Самуил Маршак')
# input.send_keys(Keys.ENTER)


books = []
while True:
    while True:
        wait = WebDriverWait(driver,30)
        cards = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//article[@class ='product-card']")))

        cards = driver.find_elements(By.XPATH, "//article[@class ='product-card']")  # 100
        print(len(cards))
        count = len(cards)
        driver.execute_script('window.scrollBy(0,2000)')
        time.sleep(2)
        cards = driver.find_elements(By.XPATH, "//article[@class ='product-card']")
        if len(cards) == count:
            break
    for card in cards:
        price = card.find_element(By.XPATH, "//div/span[@class ='app-price']").text
        name = card.find_element(By.XPATH, "./div/a[@class ='product-card__name']").text
        author = card.find_element(By.XPATH, "//div/a[@class ='author-list__item smartLink']").text
        url = card.find_element(By.XPATH, "./div/a").get_attribute('href')
        book_info = {
            'author': author,
            'name': name,
            'price': price,
            'url': url
        }
        books.append(book_info)
        print(author,name, price, url)
    try:
        button = driver.find_element(By.XPATH, "//li/a[@class ='pagination__item _link _button _next smartLink']").click()
        actions = ActionChains(driver)
        actions.move_to_element(button).click()
        #button.click()
        actions.perform()
    except:
        break

with open('books.json', 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False,indent=4)

print(len(books))

