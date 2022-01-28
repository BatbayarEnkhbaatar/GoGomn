from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import uuid
import constant.db as db
import constant.input_item as input
from datetime import date



####chrome driver
options = webdriver.ChromeOptions()
options.add_argument('--user-agent = Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36')
options.add_argument('--headless')
options.add_argument('window-size=3072x1920')
options.add_argument('disable-gpu')
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument('--disable-extensions')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features=AutomationControlled')
# driver = webdriver.Chrome("./driver/chromedriver", options=options)
driver = webdriver.Remote(command_executor="http://13.124.151.34:32768", options=options)
#### chrome driver

target_url = "https://gogo.mn"
driver.get(target_url)
driver.implicitly_wait(30)
print("Page has been fully loaded")
jobs = []
time.sleep(5)

page_num = 0
div_class ="back-blue uk-text-bold text-white text-16 uk-display-inline-block padding-10 uk-text-uppercase padding-left-20 padding-right-20 margin-top-40 margin-bottom-40"
gogoapp="gogoapp"
loadMoreXpath="/html/body/div[2]/div[2]/section[2]/div/div/div[1]/div/div[4]/a/div"
# loadMoreXpathhref="/html/body/div[2]/div[2]/section[2]/div/div/div[1]/div/div[4]/a"
WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, loadMoreXpath)))
while driver.find_element_by_xpath(loadMoreXpath):
    ClickHere=driver.find_element_by_xpath(loadMoreXpath)
    # ClickHere.click()
    driver.execute_script("arguments[0].click();", ClickHere)
    page_num += 1
    print("page #", page_num, " is getting read")
    time.sleep(1)

    # print("Windows size: ", driver.get_window_size())

page_num = 10
driver.quit()
print("total page # ", page_num)
# print("Windows size: ", driver.get_window_size())

current_time = date.today()
today = current_time.strftime("%b-%d-%Y")
status = "starting"
db.input_total_info(today, status, target_url, page_num)
