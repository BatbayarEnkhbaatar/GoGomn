from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

import json
import time
driver: WebDriver = webdriver.Chrome("/Users/spider/job/projects/for_test/gogomn/driver/chromedriver")
with open("jobs.json", "r") as f:
    data = json.load(f)

for item in data:
    #print ("ID: ",item["ID"])
    #link = "https://gogo.mn/r/yqq3d"
    link = item["Link"]
    driver.get(link)
    parentdiv = driver.find_element_by_xpath("//div[@class='not-short-read  uk-container uk-column-1-1 uk-column-divider seo-bagana-tablet']")

    count = len(parentdiv.find_elements_by_tag_name("p"))
    for i in range(0, count):
        t = parentdiv.find_elements_by_tag_name('p')[i]
        k = t.get_attribute("innerHTML")
        print(k)
    print(link)
    print(count)

print("GOGO ")