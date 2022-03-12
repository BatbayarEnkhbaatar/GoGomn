from selenium import webdriver
from datetime import datetime
import time
import constant.db as db
import os
import re


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def isXpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
        return True
    except:
        return False


def lambda_handler(event, context):
    # Set time zone
    os.environ['TZ'] = 'Asia/Ulaanbaatar'
    time.tzset()
    ####chrome driver
    options = webdriver.ChromeOptions()
    options.binary_location = '/opt/headless-chromium'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('/opt/chromedriver', chrome_options=options)
    target_url = "https://gogo.mn"
    new_info = "today's_new"
    numb_of_jobs = db.get_count_item(new_info)
    print(numb_of_jobs)
    for j in range(0, numb_of_jobs):
        data = db.get_a_new_job(new_info)
        print("Data: ", data)
        for item in data:
            job_id = item["job_id"]
            print(job_id)
            status = "scrapped"
            date = datetime.today()
            link = item["job_url"]
            print(link)
            driver.get(link)
            published_date = {}
            status = "executed"
            db.update_crawling_results(job_id, status, link, str(date))
            if isXpath("//*[@id='news-morebody']/div[1]/h1"):
                # To get the title
                article_title_xpath = driver.find_element_by_xpath("//*[@id='news-morebody']/div[1]/h1").get_attribute(
                    "innerHTML")
                article_title = {
                    'title': article_title_xpath.strip()
                }
                article_title = {
                    'title': "untitled"
                }
            print(article_title)
            else:
            if isXpath("//*[@class='text-gray text-12 uk-text-uppercase margin-top-5']"):

                published_date_xpath = driver.find_element_by_xpath(
                    "//*[@class='text-gray text-12 uk-text-uppercase margin-top-5']")
                published_date = {
                    'published_date': published_date_xpath.get_attribute("innerHTML")
                }
            else:
                published_date = {
                    'published_date': "unknown"
                }
            print("published_date: ", published_date)
            if isXpath('//*[@id="news-morebody"]/div[1]/div[3]/div[1]/div/div/a/div/div/div[1]'):
                jouarnalist_xpath = driver.find_element_by_xpath(
                    '//*[@id="news-morebody"]/div[1]/div[3]/div[1]/div/div/a/div/div/div[1]')
                jouarnalist_name = {
                    'journalist': jouarnalist_xpath.get_attribute("innerHTML")
                }
            else:
                jouarnalist_name = "unknown"
            print("Setguulch: ", jouarnalist_name)
            if isXpath("//*[@class='not-short-read  uk-container uk-column-1-1 uk-column-divider seo-bagana-tablet']"):
                parentdiv = driver.find_element_by_xpath(
                    "//*[@class='not-short-read  uk-container uk-column-1-1 uk-column-divider seo-bagana-tablet']")
                count = len(parentdiv.find_elements_by_tag_name("p"))
                content = ""
                for i in range(0, count):
                    t = parentdiv.find_elements_by_tag_name('p')[i]
                    content_text = cleanhtml(t.get_attribute("innerHTML"))
                    content = content + " " + content_text
                    article_title = str(article_title)
                db.put_items_scraping_results(job_id, status, article_title, str(content), str(published_date),
                                              jouarnalist_name)
                job_status = "completed"
                db.update_crawling_results(job_id, status, link, str(date))
                print("The job id: ", job_id, " is completed")
            else:
                job_status = "incompleted"
                db.update_crawling_results(job_id, status, link, str(date))
            content = ""
    date = datetime.today()
    driver.quit()
    driver.close()
    return str(numb_of_jobs) + " distinct news scrapped from gogomn"
