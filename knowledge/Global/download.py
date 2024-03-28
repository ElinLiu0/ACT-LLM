#Author: Elin
#Date: 2024-03-27 21:13:19
#Last Modified by:   Elin
#Last Modified time: 2024-03-27 21:13:19
from selenium.webdriver import Chrome,ChromeOptions
import json
import time
import subprocess
import os
import random

source = json.loads(open("./github_issues.json","r").read())

options = ChromeOptions()
options.add_argument("--headless")

driver = Chrome(options=options)


def search(url:str,doctype:str) -> None:
    driver.get(url=url)
    print(url,doctype)
    time.sleep(5)
    container = driver.find_element_by_tag_name("main")
    print(container)
    issues = container.find_elements_by_class_name("Box-row")
    print(len(issues))
    for issue in issues:
        title = issue.find_element_by_class_name("Link--primary").text

        title = title.replace("/","-").replace("\\","-").replace(":","-").replace("*","-").replace("?","-").replace("\"","-").replace("<","-").replace(">","-").replace("|","-")
        title = title.replace(" ","_")
        url = issue.find_element_by_class_name("Link--primary").get_attribute("href")
        print(title,url)
        print("Downloading...")

        if os.path.exists(f"./original-source/{doctype}/{title}.html"):
            print("Already downloaded")
            break
        subprocess.run(["curl","-o",f"./original-source/{doctype}/{title}.html",f"{url}"])

        print("Downloaded")
        time.sleep(random.randint(1,5))
for application in source:
    print(application)
    if application["open_pages"] == 1:
        search(application["open_url"],application["doc_category"])
    else:
        pages = application["open_pages"]
        for page in range(1,pages+1):
            search(application['open_url'].format(page),application["doc_category"])
        
    if application["closed_pages"] == 1:
        search(application["closed_url"],application["doc_category"])
    else:
        pages = application["closed_pages"]
        for page in range(1,pages+1):
            search(application['closed_url'].format(page),application["doc_category"])

driver.quit()