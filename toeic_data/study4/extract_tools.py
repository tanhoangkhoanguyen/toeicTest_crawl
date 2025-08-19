import os, cloudscraper, json, re
from bs4 import BeautifulSoup


DIRECTORY = "toeic_data/study4"
FOLDER_FORMAT = "_study4"
scraper = cloudscraper.create_scraper()


# ==========  TOOLS  ==========
def extract_audio(soup, key, folder):
    file_url = soup.find(key).get('src')
    if file_url == None:
        return extract_audio(soup, "source", folder)
    file_name = os.path.basename(file_url)
    save_file_path = f"{DIRECTORY}/listening/L{folder}/audio/{file_name}"
        
    try:
        file_data = scraper.get(file_url).content
        with open(save_file_path, "wb") as f:
            f.write(file_data)
        print(f"Downloaded {file_url} -> {save_file_path}")
    except Exception as e:
        print(f"Failed to download {file_url}: {e}")
    
    return save_file_path


def extract_img(dir, soup, trial_time = False):
    save_file_path = ""
    img_tag = soup if soup.name == "img" else soup.find("img")

    if img_tag:
        try:
            if trial_time == True:
                img_tag["error"]
            file_url = img_tag["src"]
        except:
            try:
                file_url = img_tag["data-src"]
            except:
                return ""
        file_name = os.path.basename(file_url)
        save_file_path = f"{dir}/img/{file_name}"
        
        try:
            file_data = scraper.get(file_url).content
            with open(save_file_path, "wb") as f:
                f.write(file_data)
            print(f"Downloaded {file_url} -> {save_file_path}")
        except Exception as e:
            if trial_time == False:
                return extract_img(dir, soup, True)
            print(f"Failed to download {file_url}: {e}")
    return save_file_path


def clean_text(passage_tag):
    passage = passage_tag.get_text(separator = "\n").replace("\xa0", " ")
    passage = re.sub(r"[ \t]+", " ", passage)
    passage = re.sub(r"\n+", "\n", passage)
    passage = passage.strip()
    return passage

# ==========  EXTRACT BY PART  ==========
def extract_test_part1(soup, json_info, folder, question_id):
    save_img_path = extract_img(f"{DIRECTORY}/listening/{folder}", soup)
    json_info['items'].append({
        "part": 1, 
        "question_range": f"{question_id}-{question_id}",
        "part_image": [save_img_path],
        "questions": [{
            "question_id": question_id,
            "content": "",
            "options": ["A.", "B.", "C.", "D."]
        }]
    })

    return json_info


def extract_test_part2(json_info, question_id):
    json_info['items'].append({
        "part": 2, 
        "question_range": f"{question_id}-{question_id}",
        "part_image": [],
        "questions": [{
            "question_id": question_id,
            "content": "",
            "options": ["A.", "B.", "C."]
        }]
    })

    return json_info


def extract_test_part34(soup, json_info, folder, question_id, question_part):
    save_img_path = extract_img(f"{DIRECTORY}/listening/{folder}", soup.find_previous("div", class_ = "context-wrapper"))
    questions = []
    for i in range (3):
        soup = soup.find_next("div", class_ = "question-text")
        question = soup.text.strip()
        options = []
        for _ in range (4):
            soup = soup.find_next("div", class_ = "form-check")
            options.append(soup.text.strip())
        
        questions.append({
            "question_id": question_id + i,
            "content": question,
            "options": options
        })

    json_info['items'].append({
        "part": question_part, 
        "question_range": f"{question_id}-{question_id + 2}",
        "part_image": [save_img_path] if save_img_path != "" else [],
        "questions": questions
    })

    return json_info


def extract_test_part5(soup, json_info, question_id):
    question = soup.find_next("div", class_ = "question-text").text.strip()
    options = []
    for _ in range (4):
        soup = soup.find_next("div", class_ = "form-check")
        options.append(soup.text.strip())

    json_info['items'].append({
        "part": 5, 
        "question_range": f"{question_id}-{question_id}",
        "part_image": [],
        "part_table": [],
        "context": "",
        "questions": [{
            "question_id": question_id,
            "content": question,
            "options": options
        }]
    })

    return json_info


def extract_test_part6(soup, json_info, folder, question_id):
    text = soup.find_previous("div", class_ = "context-wrapper")
    save_img_path = extract_img(f"{DIRECTORY}/reading/{folder}", text)
    for br in text.find_all("br"):
        br.replace_with('\n')
    context = clean_text(text)
    
    questions = []
    for i in range (4):
        options = []
        for _ in range (4):
            soup = soup.find_next("div", class_ = "form-check")
            options.append(soup.text.strip())
        questions.append({
            "question_id": question_id + i,
            "content": "",
            "options": options
        })
    
    json_info['items'].append({
        "part": 6, 
        "question_range": "131-146",
        "part_image": [save_img_path],
        "part_table": [],
        "context": context,
        "questions": questions
    })
    return json_info


def extract_test_part7(soup, json_info, folder):
    part_img = []
    part_table = []

    context_tag = soup.find("div", class_ = "context-wrapper")
    for img_tag in context_tag.find_all("img"):
        part_img.append(extract_img(f"{DIRECTORY}/reading/R{folder}", img_tag))

    for table_tag in context_tag.find_all("table"):
        rows = len(table_tag.find_all('tr'))
        if rows < 1: 
            continue
        cols = len(table_tag.find_all('td')) // rows

        sub_table = {}
        data = table_tag.find_all('td')
        for j in range (1, cols + 1):
            key = clean_text(data[j - 1])
            sub_table[key] = []
            for i in range (1, rows + 1):
                sub_table[key].append(clean_text(data[cols * (i - 1) + j - 1]))

        part_table.append(sub_table)
        table_tag.extract()
    context = clean_text(context_tag)

    questions = []
    question_tabs = soup.find_all("div", class_ = "question-item-wrapper")
    start_question_id = 10000
    end_question_id = -1
    for question_tab in question_tabs:
        question_id = int(question_tab.find("div", class_ = "question-number").text.strip())
        start_question_id = min(question_id, start_question_id)
        end_question_id   = max(question_id, end_question_id)
        content = question_tab.find("div", class_ = "question-text").text.strip()
        
        options = []
        for _ in range (4):
            soup = soup.find_next("div", class_ = "form-check")
            options.append(soup.text.strip())

        questions.append({
                "question_id": question_id,
                "content": content,
                "options": options
            })
        
    json_info.append({
        "part": 7, 
        "question_range": f"{start_question_id}-{end_question_id}",
        "part_image": part_img,
        "table": part_table,
        "context": context,
        "questions": questions
    })
    return len(question_tabs), json_info


def extract_answer(test_id, json_listening_info, json_reading_info):
    with open(f"{DIRECTORY}/raw_html/{test_id}_study4/raw_answer.html", encoding = "utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    question_tabs = soup.find_all("div", class_ = "mt-2 text-success")
    answers = []
    for question_tab in question_tabs:
        answer = question_tab.text.strip()
        answers.append(answer[-1])

    question_id = 0
    for item in json_listening_info["items"]:
        for question in item["questions"]:
            question["answer"] = answers[question_id]
            question_id += 1
            
    for item in json_reading_info["items"]:
        for question in item["questions"]:
            question["answer"] = answers[question_id]
            question_id += 1
    
    json_store_path = f"{DIRECTORY}/listening/L{test_id + FOLDER_FORMAT}/parser_output.json"
    with open(json_store_path, "w", encoding = "utf-8") as f:
        print (json.dumps(json_listening_info, indent = 4), file = f)

    json_store_path = f"{DIRECTORY}/reading/R{test_id + FOLDER_FORMAT}/parser_output.json"
    with open(json_store_path, "w", encoding = "utf-8") as f:
        print (json.dumps(json_reading_info, indent = 4), file = f)


# ==========  EXTRACT BY TYPE  ==========
def extract_test(tests_format, test_id):
    with open(f"{DIRECTORY}/raw_html/{test_id + FOLDER_FORMAT}/raw_test.html", encoding = "utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    save_audio_path = extract_audio(
        soup, 
        "audio", 
        f"{test_id + FOLDER_FORMAT}"
    )
    json_listening_info = {
        "test_id": test_id,
        "audio": save_audio_path,
        "items": []
    }
    json_reading_info = {
        "test_id": test_id,
        "items": []
    }

    question_tabs = soup.find_all("div", class_ = "question-item-wrapper")
    question_id = 0
    first_question_id = -1
    for question_tab in question_tabs:
        question_id += 1
        if question_id <= tests_format[0]:
            json_listening_info = extract_test_part1(
                question_tab, 
                json_listening_info, 
                f"L{test_id + FOLDER_FORMAT}", 
                question_id
            )
        elif question_id <= tests_format[1]:
            json_listening_info = extract_test_part2(
                json_listening_info, 
                question_id
            )
        elif question_id <= tests_format[2]:
            if question_id == tests_format[1] + 1:
                first_question_id = question_id % 3
            if question_id % 3 == first_question_id:
                json_listening_info = extract_test_part34(
                    question_tab, 
                    json_listening_info, 
                    f"L{test_id + FOLDER_FORMAT}", 
                    question_id, 
                    3
                )
        elif question_id <= tests_format[3]:
            if question_id == tests_format[2] + 1:
                first_question_id = question_id % 3
            if question_id % 3 == first_question_id:
                json_listening_info = extract_test_part34(
                    question_tab, 
                    json_listening_info, 
                    f"L{test_id + FOLDER_FORMAT}", 
                    question_id, 
                    4
                )
        elif question_id <= tests_format[4]:
            json_reading_info = extract_test_part5(
                question_tab, 
                json_reading_info,
                question_id
            )
        elif question_id <= tests_format[5]:
            if question_id == tests_format[4] + 1:
                first_question_id = question_id % 4
            if question_id % 4 == first_question_id:
                json_reading_info = extract_test_part6(
                    question_tab, 
                    json_reading_info, 
                    f"R{test_id + FOLDER_FORMAT}", 
                    question_id
                )
        else:
            break

    question_tabs = soup.find_all("div", class_ = "question-group-wrapper")
    json_part7 = []
    for r in range(len(question_tabs) - 1, 0, -1):
        question_tab = question_tabs[r]
        x, json_part7 = extract_test_part7(
            question_tab, 
            json_part7, 
            f"{test_id + FOLDER_FORMAT}"
        )
        question_id += x
        if question_id == 201:
            break
    json_reading_info["items"] += json_part7
    extract_answer(test_id, json_listening_info, json_reading_info)