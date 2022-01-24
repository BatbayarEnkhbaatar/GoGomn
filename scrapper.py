from selenium import webdriver
from datetime import datetime
import contants.db as db
import re
import contants.constants as const
options = webdriver.ChromeOptions()
options.add_argument(
    '--user-agent = Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36')
# options.add_argument('--headless')
# options.add_argument('window-size=3072x19272x1920')
options.add_argument('disable-gpu')
# options.add_argument('start-maximized')
# options.add_argument('disable-infobars')
options.add_argument('--disable-extensions')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome("./driver/chromedriver_win.exe", options=options)


# driver = webdriver.Remote(command_executor="http://13.124.151.34:32768", options=options)

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


new_info = "new_job"

numb_of_jobs = db.get_count_item("new_job")

for j in range(0, numb_of_jobs):
    data = db.get_a_new_job(new_info)
    for item in data:
        job_id = item["job_id"]
        print(job_id)
        status = "scrapped"
        date = datetime.today()
        link = item["job_url"]
        driver.get(link)
        published_date = {}
        status = "executed"
        db.update_crawling_results(job_id, status, link, str(date))
        try:
            if driver.find_element_by_xpath("//*[@id='news-morebody']/div[1]/h1").get_attribute("innerHTML"):
                article_title_xpath = driver.find_element_by_xpath("//*[@id='news-morebody']/div[1]/h1").get_attribute(
                    "innerHTML")
                article_title = {
                    'title': article_title_xpath.strip()
                }
            else:
                article_title = {
                    'title': "untitled"
                }
            if driver.find_element_by_xpath(
                    "//div[@class='text-gray text-12 uk-text-uppercase margin-top-5']").get_attribute("innerHTML"):
                published_date_xpath = driver.find_element_by_xpath(
                    "//div[@class='text-gray text-12 uk-text-uppercase margin-top-5']")
                published_date = {
                    'published_date': published_date_xpath.get_attribute("innerHTML")
                }
            else:
                published_date = {
                    'published_date': "unknown"
                }
            print(published_date)
            if driver.find_element_by_xpath(
                    "//div[@class='not-short-read  uk-container uk-column-1-1 uk-column-divider seo-bagana-tablet']"):
                # print(len(driver.find_element_by_xpath("//div[@class='not-short-read  uk-container uk-column-1-1 uk-column-divider seo-bagana-tablet']")))
                parentdiv = driver.find_element_by_xpath(
                    "//div[@class='not-short-read  uk-container uk-column-1-1 uk-column-divider seo-bagana-tablet']")
                count = len(parentdiv.find_elements_by_tag_name("p"))
                for i in range(0, count):
                    t = parentdiv.find_elements_by_tag_name('p')[i]
                    content_text = cleanhtml(t.get_attribute("innerHTML"))
                    content = content + " " + content_text
                    article_title = str(article_title)
                    # article_title = article_title.strip()
                db.put_items_scraping_results(job_id, status, article_title, str(content), str(published_date))
                job_status = "completed"
                db.update_crawling_results(job_id, status, link, str(date))
            else:
                job_status = "incompleted"
                db.update_crawling_results(job_id, status, link, str(date))
            content = ""
        except:
            pass
date = datetime.today()
db.put_last_scraped_time(link, date)
db.put_items_total_info(date, numb_of_jobs)
