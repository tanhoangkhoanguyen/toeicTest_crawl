import os, cloudscraper, json, re
from bs4 import BeautifulSoup


scraper = cloudscraper.create_scraper()


# ==========  TOOLS  ==========
def extract_audio(soup, key, folder):
    file_url = soup.find(key).get('src')
    if file_url == None:
        return extract_audio(soup, "source", folder)
    file_name = os.path.basename(file_url)
    save_file_path = f"crawled_html/{folder}/audio/{file_name}"
        
    try:
        file_data = scraper.get(file_url).content
        with open(save_file_path, "wb") as f:
            f.write(file_data)
        print(f"Downloaded {file_url} -> {save_file_path}")
    except Exception as e:
        print(f"Failed to download {file_url}: {e}")
    
    return save_file_path


def extract_img(soup, key, folder):
    save_file_path = ""
    img_tag = soup if soup.name == "img" else soup.find("img")

    if img_tag:
        file_url = img_tag.get(key)
        if file_url == None:
            if key != "data-src":
                return extract_img(soup, "data-src", folder)
            return ""
        file_name = os.path.basename(file_url)
        save_file_path = f"crawled_html/{folder}/img/{file_name}"
        
        try:
            file_data = scraper.get(file_url).content
            with open(save_file_path, "wb") as f:
                f.write(file_data)
            print(f"Downloaded {file_url} -> {save_file_path}")
        except Exception as e:
            print(f"Failed to download {file_url}: {e}")
    
    return save_file_path


def clean_text(passage_tag):
    passage = passage_tag.get_text(separator = "\n").replace("\xa0", " ")
    passage = re.sub(r"[ \t]+", " ", passage)
    passage = re.sub(r"\n+", "\n", passage)
    passage = passage.strip()
    return passage

# ==========  EXTRACT BY PART  ==========
def extract_test_part1(soup, json_info, folder, id):
    save_img_path = extract_img(soup, "src", folder)
    json_info['part_1'][str(id)] = {
        "image": save_img_path,
        "options": ["A.", "B.", "C.", "D."]
    }

    return json_info


def extract_test_part2(json_info, id):
    json_info['part_2'][str(id)] = {
        "options": ["A.", "B.", "C."]
    }

    return json_info


def extract_test_part345(soup, json_info, folder, id, part):
    save_img_path = extract_img(soup.find_previous("div", class_ = "context-wrapper"), "img", folder) if id % 3 > 1 and part < 5 else ""
    question = soup.find_next("div", class_ = "question-text").text.strip()
    options = []
    for _ in range (4):
        soup = soup.find_next("div", class_ = "form-check")
        options.append(soup.text.strip())

    json_info[f'part_{part}'][str(id)] = {
        "image": save_img_path,
        "question": question,
        "options": options
    } if part < 5 else {
        "question": question,
        "options": options
    }

    return json_info


def extract_test_part6(soup, json_info, folder, id):
    passage = ""
    save_img_path = ""
    if id % 4 > 2:
        text = soup.find_previous("div", class_ = "context-wrapper")
        save_img_path = extract_img(text, 'src', folder)
        for br in text.find_all("br"):
            br.replace_with('\n')
        passage = str(text.get_text().strip())
        passage = re.sub(r'[ \t]+', ' ', passage)
        passage = re.sub(r'\n\s+', '\n', passage)
    
    options = []
    for _ in range (4):
        soup = soup.find_next("div", class_ = "form-check")
        options.append(soup.text.strip())
    
    json_info['part_6'][str(id)] = {
        "passage": passage,
        "img": save_img_path,
        "options": options
    }

    return json_info


def extract_test_part7(soup, json_info, folder):
    table = {}
    img = {}
    nums = 0

    context_tag = soup.find("div", class_ = "context-wrapper")
    for i, img_tag in enumerate(context_tag.find_all("img")):
        # print ("Meow meow", end = "    ")
        # print (img_tag)
        img[str(i + 1)] = extract_img(img_tag, 'src', folder)

    for table_tag in context_tag.find_all("table"):
        nums += 1
        table[str(nums)] = {}

        rows = len(table_tag.find_all('tr'))
        cols = len(table_tag.find_all('td')) // rows
        
        table[str(nums)]["rows"] = rows
        table[str(nums)]["cols"] = cols
        data = table_tag.find_all('td')
        for i in range (1, rows + 1):
            for j in range (1, cols + 1):
                table[str(nums)][f"{i}_{j}"] = clean_text(data[cols * (i - 1) + j - 1])

        table_tag.extract()
    
    passage = clean_text(context_tag)

    num = 0
    for question_tab in soup.find_all("div", class_ = "question-item-wrapper"):
        num += 1

        i = question_tab.find("div", class_ = "question-number").text.strip()
        question = question_tab.find("div", class_ = "question-text").text.strip()

        options = []
        for _ in range (4):
            soup = soup.find_next("div", class_ = "form-check")
            options.append(soup.text.strip())

        json_info[str(i)] = {
            "img": img if num == 1 else "",
            "passage": passage if num == 1 else "",
            "table": table if num == 1 else {},
            "question": "question",
            "option": options
        }

    return num, json_info


# ==========  EXTRACT BY TYPE  ==========
def extract_test(key):
    with open(f"crawled_html/{key}/raw_test.html", encoding = "utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    title = soup.find("h1").text.strip()
    digit = re.search(r'\d+', title)
    if digit:
        title = title[:digit.end()]
    save_audio_path = extract_audio(soup, "audio", key)

    json_info = {
        "title": title,
        "audio": save_audio_path,
        "part_1": {},
        "part_2": {},
        "part_3": {},
        "part_4": {},
        "part_5": {},
        "part_6": {},
        "part_7": {},
    }

    question_tabs = soup.find_all("div", class_ = "question-item-wrapper")
    i = 0
    for question_tab in question_tabs:
        i += 1
        if i < 7:
            json_info = extract_test_part1(question_tab, json_info, key, i)
        elif i < 32:
            json_info = extract_test_part2(json_info, i)
        elif i < 71:
            json_info = extract_test_part345(question_tab, json_info, key, i, 3)
        elif i < 101:
            json_info = extract_test_part345(question_tab, json_info, key, i, 4)
        elif i < 131:
            json_info = extract_test_part345(question_tab, json_info, key, i, 5)
        elif i < 147:
            json_info = extract_test_part6(question_tab, json_info, key, i)
        else:
            break

    question_tabs = soup.find_all("div", class_ = "question-group-wrapper")
    json_part7 = {}
    for r in range(len(question_tabs) - 1, 0, -1):
        question_tab = question_tabs[r]
        x, json_part7 = extract_test_part7(question_tab, json_part7, key)
        i += x
        if i == 201:
            break
    
    i = 147
    while True:
        if i == 201:
            break
        json_info["part_7"][str(i)] = json_part7[str(i)]
        i += 1


    json_store_path = f"crawled_html/{key}/test_parser_output.json"
    with open(json_store_path, "w", encoding = "utf-8") as f:
        print (json.dumps(json_info, indent = 4), file = f)
        

def extract_answer(key):
    with open(f"crawled_html/{key}/raw_answer.html", encoding = "utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    json_info = {
        "part_1": {},
        "part_2": {},
        "part_3": {},
        "part_4": {},
        "part_5": {},
        "part_6": {},
        "part_7": {},
    }
    question_tabs = soup.find_all("div", class_ = "mt-2 text-success")
    i = 0
    j = 1
    for question_tab in question_tabs:
        i += 1
        answer = question_tab.text.strip()
        json_info[f"part_{j}"][str(i)] = answer[-1]

        if i == 6:
            j += 1
        elif i == 31:
            j += 1
        elif i == 70:
            j += 1
        elif i == 100:
            j += 1
        elif i == 132:
            j += 1
        elif i == 146:
            j += 1
    
    json_store_path = f"crawled_html/{key}/answer_parser_output.json"
    with open(json_store_path, "w", encoding = "utf-8") as f:
        print (json.dumps(json_info, indent = 4), file = f)