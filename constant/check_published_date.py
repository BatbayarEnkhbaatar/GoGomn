from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
import time
import uuid
import db
import constants as const
import re


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    cleantext = cleantext.replace("&nbsp;", "").replace("·", "")
    return cleantext


####chrome driver
options = webdriver.ChromeOptions()
# options.add_argument('--user-agent = Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36')
options.add_argument('--headless')
options.add_argument('window-size=3072x1920')
options.add_argument('disable-gpu')
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument('--disable-extensions')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
# options.add_experimental_option('useAutomationExtension', False)
# options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome("./driver/chromedriver_win.exe", options=options)
# driver = webdriver.Remote(command_executor="http://13.124.151.34:32768", options=options)
#### chrome driver

target_url = "https://gogo.mn"
driver.get(target_url)
driver.implicitly_wait(30)
print("Page has been fully loaded")
jobs = []
time.sleep(5)
date_today = datetime.today()
link_num = 20
start_link_num = 1
sincewhen = "2022-01-21-00-00-00"
div_class = "back-blue uk-text-bold text-white text-16 uk-display-inline-block padding-10 uk-text-uppercase padding-left-20 padding-right-20 margin-top-40 margin-bottom-40"
gogoapp = "gogoapp"
loadMoreXpath = "/html/body/div[2]/div[2]/section[2]/div/div/div[1]/div/div[4]/a/div"

time_terms = const.gogo_date_terms.terms


def check_published_date():
    get_published_time = driver.find_element_by_xpath('.//div[@class="text-gray"]').get_attribute("innerHTML")
    cleared_time = get_published_time
    c = cleanhtml(cleared_time)
    b = c.strip()
    d = b.strptime(b, '%Y-%m-%d-%H-%M-%S')
    sincewhen = db.get_last_scrapped("4qer")
    sincewhen = sincewhen.get("last_scraped")
    sincewhen = datetime.strptime(sincewhen, '%Y-%m-%d-%H-%M-%S')
    for tm in time_terms:
        b = datetime.today()
        if tm == str(b):
            print("news #", i, "exported successfully", b, "shine medee")
            return True, b
        else:
            if sincewhen > d:
                return True, d
                print("news #", i, "exported successfully", b, "shine medee")
            else:
                print("news #", i, "exported successfully", b, "huuchin medee")
                return False


print(check_published_date())