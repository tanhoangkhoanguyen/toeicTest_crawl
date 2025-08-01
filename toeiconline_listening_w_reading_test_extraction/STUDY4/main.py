from toeiconline_listening_w_reading_test_extraction.STUDY4.crawl import crawl_html
from toeiconline_listening_w_reading_test_extraction.STUDY4.url_store import url_dict
from toeiconline_listening_w_reading_test_extraction.STUDY4.extract_tools import extract_test, extract_answer


crawl_html()
for type in url_dict:
    for key, _ in type["url"].items():
        extract_test(type["parts_number"], key)
        extract_answer(type["parts_number"], key)