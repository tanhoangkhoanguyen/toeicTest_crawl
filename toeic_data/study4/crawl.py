from toeic_data.study4.authenticate import log_in
from toeic_data.study4.url_store import url_dict


import os, time
import undetected_chromedriver as uc


DIRECTORY = "toeic_data/study4"


def create_folder_url():
    # ==========  CREATE FOLDER, URL  ==========
    for type in url_dict:
        for key, _ in type["url"].items():
            os.makedirs(f"{DIRECTORY}/listening/{key}/audio", exist_ok = True)
            os.makedirs(f"{DIRECTORY}/listening/{key}/img", exist_ok = True)
            os.makedirs(f"{DIRECTORY}/reading/{key}/img", exist_ok = True)
            os.makedirs(f"{DIRECTORY}/raw_html/{key}", exist_ok = True)

    print ('=' * 10, f" FINISH CREATING FOLDER ", '=' * 10)


def crawl_html():
    create_folder_url()
    driver = log_in()

    # ==========  CRAWL  ==========
    for type in url_dict:    
        for key, value in type["url"].items():
            driver.get(value[0])
            time.sleep(1)
            raw_html = driver.page_source
            with open(f"{DIRECTORY}/raw_html/{key}/raw_test.html", "w", encoding = "utf-8") as f:
                f.write(raw_html)

            driver.get(value[1])
            time.sleep(1)
            raw_html = driver.page_source
            with open(f"{DIRECTORY}/raw_html/{key}/raw_answer.html", "w", encoding = "utf-8") as f:
                f.write(raw_html)


    def silent_del(self):
        try:
            self.quit()
        except:
            pass
    uc.Chrome.__del__ = silent_del