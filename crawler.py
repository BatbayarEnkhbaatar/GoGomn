from selenium import webdriver
from datetime import datetime
import time
import uuid
import constant.db as db
import constant.constants as const
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
div_class = "back-blue uk-text-bold text-white text-16 uk-display-inline-block padding-10 uk-text-uppercase padding-left-20 padding-right-20 margin-top-40 margin-bottom-40"
gogoapp = "gogoapp"
loadMoreXpath = "/html/body/div[2]/div[2]/section[2]/div/div/div[1]/div/div[4]/a/div"

time_terms = const.gogo_date_terms.terms

scrape_info = db.get_last_scrapped("gogoapp")
print(scrape_info)
sincewhen = datetime.strptime(scrape_info, '%Y-%m-%d %H:%M')

def check_published_date(found_date):
    cleared_time = found_date
    c = cleanhtml(cleared_time)
    b = c.strip()

    for key, value in time_terms.items():
        if key == str(b):
            b = value
            return [True, b]
            break
    if datetime.strptime(b, '%Y-%m-%d %H:%M') > sincewhen:
        return [True, b]
    else:
        return [False, b]



today_news = []
zeo = 1
last_news_dt = ""
for i in range(zeo,100):
    get_att = driver.find_element_by_xpath(
        '/html/body/div[2]/div[2]/section[2]/div/div/div[1]/div/div[4]/article[' + str(i) + ']/a')
    date_xpath = driver.find_element_by_xpath(
        './/article['+str(i)+']/a/div/div[2]/div/div[@class="text-gray"]')
    pdate = date_xpath.get_attribute("innerHTML")
    pdate_1 = cleanhtml(pdate)
    pdate_2 = pdate_1.strip()
    # print(pdate_2)
    job_id = uuid.uuid4()
    status = "new_job"
    link = get_att.get_attribute('href')
    istoday= check_published_date(pdate_2)[0]
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M')
    published_date=check_published_date(pdate_2)[1]
    if istoday==True:
        db.put_items_crawling_results(str(job_id), status, link, str(published_date))
        print("imported link ", link)
        print("published date ", published_date)
        last_news_dt = published_date
    else:
        print("Totall: ", i, current_date)
        db.put_items_last_scraped(gogoapp, current_date, i)
        break
    if driver.find_element_by_xpath(loadMoreXpath):
        ClickHere = driver.find_element_by_xpath(loadMoreXpath)
        driver.execute_script("arguments[0].click();", ClickHere)
        time.sleep(1)
    start_link_num = link_num
    link_num += 8
