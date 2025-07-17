import os
    
    
# ==========  CREATE FOLDER  ==========
for i in range (1, 2):
    os.makedirs(f"crawled_html/New Economy TOEIC Test {i}/img", exist_ok = True)
    os.makedirs(f"crawled_html/New Economy TOEIC Test {i}/audio", exist_ok = True)

print ('=' * 10, f" FINISH CREATING FOLDER ", '=' * 10)

url_dict = {
    "New Economy TOEIC Test 1": [
        "https://study4.com/tests/224/start/",
        "https://study4.com/tests/224/new-economy-toeic-test-1/solutions/"
    ]
}