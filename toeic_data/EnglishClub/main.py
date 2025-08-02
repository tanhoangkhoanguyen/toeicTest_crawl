# ========== TOEIC LINK          ========== -> https://www.englishclub.com/esl-exams/ets-toeic-practice.php               |
#                                              https://study4.com/                                                        |
#                                              https://testtoeic.com/tests/toeic.html                                     |
# ________________________________________________________________________________________________________________________|

from tools import *
from setup import *

import cloudscraper, json
from bs4 import BeautifulSoup


scraper = cloudscraper.create_scraper()


def extract_topic(json_info, soup):
    h1_title = soup.find_all("h1")
    title = str(h1_title[0].text.strip())

    p_description = h1_title[0].find_next("p")
    description = str(p_description.text.strip())

    # JSON store
    json_info["title"] = title
    json_info["description"] = description
    return json_info


def extract_example(json_info, soup, id):
    h2s = soup.find_all("h2")

    for h2 in h2s:

        title = str(h2.text.strip()).replace(' ', '_').lower()

        # task
        h2, instruction_1 = crawl_instruction(h2, "First")
        save_image_path = crawl_file(h2, "img", "img", id)
        save_audio_path = crawl_file(h2, "audio", "audio", id)
        h2, instruction_2 = crawl_instruction(h2, "Next")
        h2, body = crawl_body(h2, "clr-blue")
        
        # explanation
        explanation = {}
        looping_times = max(1, len(body))
        i = 0

        for _ in range (looping_times):
            i += 1
            explanation[f"{i}"] = []

            h2 = h2.find_next("ul")
            for ul in h2:
                text = ' '.join(ul.stripped_strings)
                if text:
                    explanation[f"{i}"].append(text)
            
            h2 = h2.find_next("p")
            answer = h2.text.strip()
            explanation[f"{i}"].append(answer)

        transcript = crawl_transcript(h2, "clr-red", "transcript:")
        
        # JSON store
        json_info[title] = {
            "instruction_1": instruction_1,
            "image": save_image_path,
            "instruction_2": instruction_2,
            "audio": save_audio_path,
            "questions": body,
            "explanation": explanation,
            "transcript": transcript
        }
            
    return json_info


def func ():
    # ==========  HTML CRAWLING  ==========
    i = 0
    for url_path in url_list:
        resp = scraper.get(url_path)
        soup = BeautifulSoup(resp.text, "html.parser")
    
        i += 1
        with open(f"crawled_html/Part {i}/raw.html", "w", encoding = "utf-8") as f:
            f.write(soup.prettify())
        print ('=' * 10, f" FINISH CRAWLING HTML Part {i} ", '=' * 10)
        

        # ==========  INFOMATION EXTRACTION  ==========
        json_info = {}
        json_info = extract_topic(json_info, soup)
        json_info = extract_example(json_info, soup, i)

        json_store_path = f"crawled_html/Part {i}/parser_output.json"
        with open(json_store_path, "w", encoding = "utf-8") as f:
            print (json.dumps(json_info, indent = 4), file = f)

    print ('=' * 10, f" FINISH EXTRACTING ", '=' * 10)


if "__main__" == __name__:
    func()