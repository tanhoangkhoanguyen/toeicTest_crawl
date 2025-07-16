import os
    
    
# ==========  CREATE FOLDER  ==========
for i in range (1, 5):
    os.makedirs(f"crawled_html/Part {i}/img", exist_ok = True)
    os.makedirs(f"crawled_html/Part {i}/audio", exist_ok = True)

print ('=' * 10, f" FINISH CREATING FOLDER ", '=' * 10)

url_list = []
for i in range(1, 5):
    url_list.append(f"https://www.englishclub.com/esl-exams/ets-toeic-practice-{i}.php")