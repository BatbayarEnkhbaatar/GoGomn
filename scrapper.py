from selenium import webdriver
from datetime import datetime
import contants.db as db
import re
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
driver = webdriver.Chrome("./driver/chromedriver", options=options)
# driver = webdriver.Remote(command_executor="http://13.124.151.34:32768", options=options)

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

new_info = "new_job"

numb_of_jobs = db.get_count_item("new_job")
content = ""

for j in range(0, numb_of_jobs):
        data = db.get_a_new_job(new_info)
        for item in data:
            job_id=item["job_id"]
            print(job_id)
            status = "scrapped"
            date = datetime.today()
            link = item["job_url"]
            driver.get(link)
            article_title_xpath = driver.find_element_by_xpath(
                "//*[@id='news-morebody']/div[1]/h1")
            article_title = {
            'title': article_title_xpath.get_attribute("innerHTML")
            }
            if len(driver.find_element_by_xpath("//div[@class='text-gray text-12 uk-text-uppercase margin-top-5']"))!=0:
                published_date_xpath = driver.find_element_by_xpath("//div[@class='text-gray text-12 uk-text-uppercase margin-top-5']")
                published_date = {
                    'published_date': published_date_xpath.get_attribute("innerHTML")
                }
            else:
                published_date = {
                    'published_date': "unknown"
                }
            parentdiv = driver.find_element_by_xpath("//div[@class='not-short-read  uk-container uk-column-1-1 uk-column-divider seo-bagana-tablet']")
            count = len(parentdiv.find_elements_by_tag_name("p"))
            for i in range(0, count):
                t = parentdiv.find_elements_by_tag_name('p')[i]
                content_text = t.get_attribute("innerHTML")
                content = cleanhtml(content) + " " + cleanhtml(content_text)
            db.put_items_scraping_results(job_id, status, str(article_title).repalce(" ", ""),str(content), str(published_date))
        job_status = "completed"
        db.update_crawling_results(job_id, status, link, str(date))
        content = ""
