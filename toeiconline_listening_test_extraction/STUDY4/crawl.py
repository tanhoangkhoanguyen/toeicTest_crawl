import os, time
import undetected_chromedriver as uc


from authenticate import log_in
from url_store import url_dict
    

def create_folder_url():
    # ==========  CREATE FOLDER, URL  ==========
    for i in range (1, 2):
        os.makedirs(f"crawled_html/New Economy TOEIC Test {i}/img", exist_ok = True)
        os.makedirs(f"crawled_html/New Economy TOEIC Test {i}/audio", exist_ok = True)

    print ('=' * 10, f" FINISH CREATING FOLDER ", '=' * 10)


def crawl_html():
    create_folder_url()
    driver = log_in()

    # ==========  CRAWL  ==========
    for key, value in url_dict.items():
        driver.get(value[0])
        time.sleep(1)
        raw_html = driver.page_source
        with open(f"crawled_html/{key}/raw_test.html", "w", encoding="utf-8") as f:
            f.write(raw_html)

        driver.get(value[1])
        time.sleep(1)
        raw_html = driver.page_source
        with open(f"crawled_html/{key}/raw_answer.html", "w", encoding="utf-8") as f:
            f.write(raw_html)


    def silent_del(self):
        try:
            self.quit()
        except:
            pass
    uc.Chrome.__del__ = silent_del