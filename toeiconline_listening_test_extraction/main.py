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
    for i, h2 in enumerate(h2s):
        # example id
        title = str(h2.text.strip())

        # instruction_1
        instruction_1 = ""
        p_instruction_1 = h2.find_next("p")
        if "First" in str(p_instruction_1):
            h2 = p_instruction_1
            instruction_1 = str(h2.text.strip())
        
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

        # instruction_2
        instruction_2 = ""
        p_instruction_2 = h2.find_next("p")
        if "Next" in str(p_instruction_2):
            h2 = p_instruction_2
            instruction_2 = str(h2.text.strip())
        
        # explanation
        p_explanation = h2.find_next("p")
        explanation = p_explanation.text.strip()

        h2 = h2.find_next("ul")
        list_explanation = []
        for li in h2:
            text = ' '.join(li.stripped_strings)
            if text:
                list_explanation.append(text)
        
        # answer
        h2 = h2.find_next("p")
        answer = h2.text.strip()

        # transcript
        h2 = h2.find_next("p")
        text = h2.text.strip()
        if text == "Transcript:":
            h2 = h2.find_next("p")
            
        clean_text = h2.get_text(separator = '\n')
        lines = [line.strip() for line in clean_text.split('\n')]
        transcript = [line for line in lines if line and line.lower() != "transcript:"]
        
        # JSON store
        json_info[title] = {
            "instruction_1": instruction_1,
            "image": save_img_path,
            "instruction_2": instruction_2,
            "audio": save_audio_path,
            f"{explanation}": list_explanation,
            "answer": answer,
            "transcript": transcript
        }
            
    return json_info


def func ():
    # ==========  CREATE FOLDER  ==========
    for i in range (1, 5):
        os.makedirs(f"crawled_html/Part {i}/images", exist_ok = True)
        os.makedirs(f"crawled_html/Part {i}/audio", exist_ok = True)

    print ('=' * 10, f" FINISH CREATING FOLDER ", '=' * 10)


    # ==========  HTML CRAWLING  ==========
    url_list = []
    for i in range(1, 5):
        url_list.append(f"https://www.englishclub.com/esl-exams/ets-toeic-practice-{i}.php")

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