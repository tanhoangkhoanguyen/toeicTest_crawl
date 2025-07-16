# ========== EMERGENCY REFERENCE ========== -> https://ideone.com/GuVjE7                                                  |
# ========== TOEIC LINK          ========== -> https://www.englishclub.com/esl-exams/ets-toeic-practice.php               |
#                                              https://study4.com/                                                        |
#                                              https://testtoeic.com/tests/toeic.html                                     |
#                                                                                                                         |
# pip install cloudscraper                                                                                                |
# ________________________________________________________________________________________________________________________|

from tools import *
from setup import *

import os, cloudscraper, json
from bs4 import BeautifulSoup


scraper = cloudscraper.create_scraper()


def extract_topic(json_info, soup):
    h1_title = soup.find_all("h1")
    title = str(h1_title[0].text.strip())

    p_description = h1_title[0].find_next("p")
    description = str(p_description.text.strip())

    # JSON store
    json_info[title] = description
    return json_info


def extract_example(json_info, soup, id):
    h2s = soup.find_all("h2")
    for i, h2 in enumerate(h2s):
        # example id
        title = str(h2.text.strip())

        # instruction_1
        h2, instruction_1 = crawl_instruction(h2, "First")
        
        # image, audio
        save_image_path = crawl_file(h2, "img", "img", id)
        save_audio_path = crawl_file(h2, "audio", "audio", id)

        # instruction_2
        h2, instruction_2 = crawl_instruction(h2, "Next")

        # qa
        h2, qa = crawl_qa(h2, "clr-blue")
        
        # explanation
        looping_times = max(1, len(qa))
        explanation = {}
        for i in range (looping_times):
            explanation[f"{i + 1}"] = []

            h2 = h2.find_next("ul")
            for li in h2:
                text = ' '.join(li.stripped_strings)
                if text:
                    explanation[f"{i + 1}"].append(text)
            
            h2 = h2.find_next("p")
            answer = h2.text.strip()
            explanation[f"{i + 1}"].append(answer)

        # transcript
        transcript = crawl_transcript(h2, "clr-red", "transcript:")
        
        # JSON store
        json_info[title] = {
            "instruction_1": instruction_1,
            "image": save_image_path,
            "instruction_2": instruction_2,
            "audio": save_audio_path,
            "questions": qa,
            "explanation": explanation,
            "transcript": transcript
        }
            
    return json_info


def func ():
    # ==========  HTML CRAWLING  ==========
    for i, url_path in enumerate(url_list):
        resp = scraper.get(url_path)
        soup = BeautifulSoup(resp.text, "html.parser")
    
        html_store_path = f"crawled_html/Part {i + 1}/raw.html"
        with open(html_store_path, "w", encoding = "utf-8") as f:
            f.write(soup.prettify())
        print ('=' * 10, f" FINISH CRAWLING Part {i + 1} ", '=' * 10)
        

        # ==========  INFOMATION EXTRACTION  ==========
        json_info = {}
        json_info = extract_topic(json_info, soup)
        json_info = extract_example(json_info, soup, i + 1)

        json_store_path = f"crawled_html/Part {i + 1}/parser_output.json"
        with open(json_store_path, "w", encoding = "utf-8") as f:
            print (json.dumps(json_info, indent = 4), file = f)

    print ('=' * 10, f" FINISH EXTRACTING ", '=' * 10)


if "__main__" == __name__:
    func()