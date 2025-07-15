# ========== EMERGENCY REFERENCE ========== -> https://ideone.com/GuVjE7                                                  |
# ========== TOEIC LINK          ========== -> https://www.englishclub.com/esl-exams/ets-toeic-practice.php               |
#                                              https://study4.com/                                                        |
#                                              https://testtoeic.com/tests/toeic.html                                     |
#                                                                                                                         |
# pip install cloudscraper                                                                                                |
# ________________________________________________________________________________________________________________________|

import os
import cloudscraper
from bs4 import BeautifulSoup
from urllib.parse import urljoin


scraper = cloudscraper.create_scraper()
BASE_URL = "https://www.englishclub.com/"


def extract_topic(json_info, soup):
    h1_title = soup.find_all("h1")
    title = str(h1_title[0].text.strip())

    p_description = h1_title[0].find_next("p")
    description = str(p_description.text.strip())

    # JSON store
    json_info[title] = description
    print (json_info)
    return json_info


def extract_example(json_info, soup, id):
    h2s = soup.find_all("h2")
    for h2 in h2s:
        # example id
        title = str(h2.text.strip())

        # description
        p_description = h2.find_next("p")
        description = str(p_description.text.strip())
        
        # image
        img_tag = h2.find_next("img")
        save_path = ""

        if img_tag and 'src' in img_tag.attrs:
            img_url = urljoin(BASE_URL, img_tag['src'])
            img_filename = os.path.basename(img_url)
            print (img_filename)
            save_path = f"crawled_html/Part {id}/images/{img_filename}"

            try:
                img_data = scraper.get(img_url).content
                with open(save_path, "wb") as f:
                    f.write(img_data)
                print(f"Downloaded {img_url} -> {save_path}")
            except Exception as e:
                print(f"Failed to download {img_url}: {e}")
        else:
            print(f"Skipped image {title} - no <img> or missing src.")

        
        # JSON store
        json_info[title] = {
            "description": description,
            "image": save_path
        }
        print (json_info)
        return json_info


def func ():
    # ==========  CREATE FOLDER  ==========
    os.makedirs("crawled_html/Part 1/images", exist_ok = True)
    os.makedirs("crawled_html/Part 2/images", exist_ok = True)
    os.makedirs("crawled_html/Part 3/images", exist_ok = True)
    os.makedirs("crawled_html/Part 4/images", exist_ok = True)
    print ('=' * 10, f" FINISH CREATING FOLDER ", '=' * 10)


    # ==========  HTML CRAWLING  ==========
    url_list = {
        "Part 1": "https://www.englishclub.com/esl-exams/ets-toeic-practice-1.php",
        "Part 2": "https://www.englishclub.com/esl-exams/ets-toeic-practice-2.php",
        "Part 3": "https://www.englishclub.com/esl-exams/ets-toeic-practice-3.php",
        "Part 4": "https://www.englishclub.com/esl-exams/ets-toeic-practice-4.php"    
    }
    for i, (key, url_path) in enumerate(url_list.items()):
        resp = scraper.get(url_path)
        soup = BeautifulSoup(resp.text, "html.parser")
    
        store_path = f"crawled_html/{key}/raw.html"
        with open(store_path, "w", encoding = "utf-8") as f:
            f.write(soup.prettify())
        print ('=' * 10, f" FINISH CRAWLING {key} ", '=' * 10)
        

        # ==========  INFOMATION EXTRACTION  ==========
        json_info = {}
        json_info = extract_topic(json_info, soup)
        json_info = extract_example(json_info, soup, i + 1)

    print ('=' * 10, f" FINISH EXTRACTING ", '=' * 10)


if "__main__" == __name__:
    func()