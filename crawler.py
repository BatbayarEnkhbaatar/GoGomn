from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
import json
import time
import uuid

driver: WebDriver = webdriver.Chrome("/Users/spider/job/projects/for_test/gogomn/driver/chromedriver")
target_url = "https://gogo.mn/i/7"
driver.get(target_url)
jobs = []
time.sleep(5)
for i in range(1, 10):
        #titles_element = driver.find_element_by_xpath('//*[@id="gogoapp"]/div[2]/section[1]/div/div/div[1]/div[2]/div[1]/div/div[2]/article['+str(i)+']/a/div/div[2]/h4')
        #titles = titles_element.get_attribute('textContent')
        #print("Artile #", i, ":", titles)
        id = uuid.uuid4()
        get_att = driver.find_element_by_xpath(
            '//*[@id="gogoapp"]/div[2]/section[1]/div/div/div[1]/div[2]/div[1]/div/div[2]/article[' + str(i) + ']/a')
        link = get_att.get_attribute('href')
        jobs.append({
            "ID": "ID_" + str(id),
            "Link" : link
        })

with open("jobs.json", "w", encoding="utf-8") as outcomes:
    json.dump(jobs, outcomes, ensure_ascii=False)

