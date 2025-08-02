from toeic_data.study4.crawl import crawl_html
from toeic_data.study4.url_store import url_dict
from toeic_data.study4.extract_tools import extract_test, extract_answer


# crawl_html()
for type in url_dict:
    for key, _ in type["url"].items():
        extract_test(type["parts_number"], key)
        extract_answer(type["parts_number"], key)