# ========== EMERGENCY REFERENCE ========== -> https://ideone.com/GuVjE7                                                  |
# ========== TOEIC LINK          ========== -> https://www.englishclub.com/esl-exams/ets-toeic-practice.php               |
#                                              https://study4.com/                                                        |
#                                              https://testtoeic.com/tests/toeic.html                                     |
#                                                                                                                         |
# pip install cloudscraper                                                                                                |
# ________________________________________________________________________________________________________________________|

import os, cloudscraper, json
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

        # instruction_1
        p_instruction_1 = h2.find_next("p")
        instruction_1 = str(p_instruction_1.text.strip()) if p_instruction_1 else ""
        
        # image
        img_tag = h2.find_next("img")
        save_img_path = ""

        if img_tag and 'src' in img_tag.attrs:
            img_url = urljoin(BASE_URL, img_tag['src'])
            img_filename = os.path.basename(img_url)
            save_img_path = f"crawled_html/Part {id}/images/{img_filename}"

            try:
                img_data = scraper.get(img_url).content
                with open(save_img_path, "wb") as f:
                    f.write(img_data)
                print(f"Downloaded {img_url} -> {save_img_path}")
            except Exception as e:
                print(f"Failed to download {img_url}: {e}")
        else:
            print(f"Skipped image {title} - no <img> or missing src.")

        # instruction_2
        p_instruction_2 = h2.find_next("p")
        instruction_2 = str(p_instruction_2.text.strip()) if p_instruction_2 else ""
        
        # audio
        audio_tag = h2.find_next("audio")
        save_audio_path = ""

        if audio_tag and 'src' in audio_tag.attrs:
            audio_url = urljoin(BASE_URL, audio_tag['src'])
            audio_filename = os.path.basename(audio_url)
            print (audio_url, '  ', audio_filename)
            save_audio_path = f"crawled_html/Part {id}/audio/{audio_filename}"

            try:
                audio_data = scraper.get(audio_url).content
                with open(save_audio_path, "wb") as f:
                    f.write(audio_data)
                print(f"Downloaded {audio_url} -> {save_audio_path}")
            except Exception as e:
                print(f"Failed to download {audio_url}: {e}")
        else:
            print(f"Skipped image {title} - no <audio> or missing src.")
        
        # explanation
        p_explanation = h2.find_next("strong")
        explanation = p_explanation.text.strip()
        list_explanation = []

        for _ in range (3):
            h2 = h2.find_next("li")
            choice = h2.text.strip()
            list_explanation.append(str(choice))
        
        # answer
        p_answer = h2.find_next("p")
        answer = p_answer.text.strip()

        
        # JSON store
        json_info[title] = {
            "instruction_1": instruction_1,
            "image": save_img_path,
            "instruction_2": instruction_2,
            "audio": save_audio_path,
            f"{explanation}": list_explanation,
            "answer": answer
        }
    return json_info


def func ():
    # ==========  CREATE FOLDER  ==========
    os.makedirs("crawled_html/Part 1/images", exist_ok = True)
    os.makedirs("crawled_html/Part 1/audio", exist_ok = True)

    os.makedirs("crawled_html/Part 2/images", exist_ok = True)
    os.makedirs("crawled_html/Part 2/audio", exist_ok = True)

    os.makedirs("crawled_html/Part 3/images", exist_ok = True)
    os.makedirs("crawled_html/Part 3/audio", exist_ok = True)

    os.makedirs("crawled_html/Part 4/images", exist_ok = True)
    os.makedirs("crawled_html/Part 4/audio", exist_ok = True)

    print ('=' * 10, f" FINISH CREATING FOLDER ", '=' * 10)


    # ==========  HTML CRAWLING  ==========
    url_list = [
        "https://www.englishclub.com/esl-exams/ets-toeic-practice-1.php",
        "https://www.englishclub.com/esl-exams/ets-toeic-practice-2.php",
        "https://www.englishclub.com/esl-exams/ets-toeic-practice-3.php",
        "https://www.englishclub.com/esl-exams/ets-toeic-practice-4.php"    
    ]
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