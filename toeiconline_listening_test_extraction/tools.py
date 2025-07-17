from urllib.parse import urljoin
import os, cloudscraper, re


scraper = cloudscraper.create_scraper()
BASE_URL = "https://www.englishclub.com/"


def crawl_instruction(h2, key):
    instruction = ""
    p_instruction = h2.find_next("p")
    if key in str(p_instruction):
        h2 = p_instruction
        instruction = str(h2.text.strip())
    return h2, instruction


def crawl_file(h2, key, file, id):
    file_tag = h2.find_next(f"{key}")
    save_file_path = ""

    file_src = file_tag.get('src') if file_tag else None
    if not file_src:
        file_src = file_tag.get('data-cfsrc') if file_tag else None

    if file_tag and file_src:
        file_url = urljoin(BASE_URL, file_src)
        file_filename = os.path.basename(file_url)
        save_file_path = f"crawled_html/Part {id}/{file}/{file_filename}"

        try:
            file_data = scraper.get(file_url).content
            with open(save_file_path, "wb") as f:
                f.write(file_data)
            print(f"Downloaded {file_url} -> {save_file_path}")
        except Exception as e:
            print(f"Failed to download {file_url}: {e}")
    else:
        if file == "audio":
            next_tag = h2.find_next("source")
            if next_tag:
                return crawl_file(h2, "source", file, id)
        print(f"Skipped {file} - no <{key}> tag or missing src/data-cfsrc.")
        print(file_tag)

    return save_file_path
    

def crawl_qa(h2, className):
    qa = {}
    i = 0

    while True:
        p = h2.find_next("p")
        if not p or className not in p.get("class", []):
            break

        h2 = p
        lines = [line.strip() for line in p.get_text(separator="\n").split("\n")]
        lines = [line for line in lines if line]

        for line in lines:
            q_match = re.match(r'^(\d+)\.\s*(.+)', line)
            if q_match:
                i += 1
                q_num = f"{i}"
                question_text = q_match.group(2).strip()
                qa[q_num] = {
                    "question": question_text,
                    "choices": {}
                }
            elif q_num and re.match(r'^[A-D]\)', line):
                choice_letter, choice_text = line.split(")", 1)
                qa[q_num]["choices"][choice_letter.strip()] = choice_text.strip()

    return h2, qa

def crawl_transcript(h2, className, unwantedText):
    next = h2.find_next("p", class_ = className)
    if next == None:
        return []

    h2 = h2.find_next("p", class_ = className)
    text = h2.text.strip()
    if text.lower() == unwantedText:
        h2 = h2.find_next("p", class_ = className)
            
    clean_text = h2.get_text(separator = '\n')
    lines = [line.strip() for line in clean_text.split('\n')]
    transcript = [line for line in lines if line and line.lower() != unwantedText]
    return transcript