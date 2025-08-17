from toeic_data.study4.authenticate import log_in
from toeic_data.study4.url_store import url_list


import os, time
import undetected_chromedriver as uc


DIRECTORY = "toeic_data/study4"
FOLDER_FORMAT = "_study4"


def create_folder_url():
    # ==========  CREATE FOLDER, URL  ==========
    for format in url_list:
        for test_id, _ in format["url"].items():
            os.makedirs(f"{DIRECTORY}/listening/L{test_id + FOLDER_FORMAT}/audio", exist_ok = True)
            os.makedirs(f"{DIRECTORY}/listening/L{test_id + FOLDER_FORMAT}/img", exist_ok = True)
            os.makedirs(f"{DIRECTORY}/reading/R{test_id + FOLDER_FORMAT}/img", exist_ok = True)
            os.makedirs(f"{DIRECTORY}/raw_html/{test_id + FOLDER_FORMAT}", exist_ok = True)

    print ('=' * 10, f" FINISH CREATING FOLDER ", '=' * 10)

def silent_del(self):
    try:
        self.quit()
    except:
        pass

def crawl_html():
    create_folder_url()
    return
    driver = log_in()

    # ==========  CRAWL  ==========
    for format in url_list:    
        for test_id, link in format["url"].items():
            driver.get(link[0])
            time.sleep(1)
            raw_html = driver.page_source
            with open(f"{DIRECTORY}/raw_html/{test_id + FOLDER_FORMAT}/raw_test.html", "w", encoding = "utf-8") as f:
                f.write(raw_html)

            driver.get(link[1])
            time.sleep(1)
            raw_html = driver.page_source
            with open(f"{DIRECTORY}/raw_html/{test_id + FOLDER_FORMAT}_study4/raw_answer.html", "w", encoding = "utf-8") as f:
                f.write(raw_html)
            
    uc.Chrome.__del__ = silent_del