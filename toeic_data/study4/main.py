from toeic_data.study4.crawl import crawl_html
from toeic_data.study4.url_store import url_list
from toeic_data.study4.extract_tools import extract_test


crawl_html()
for format in url_list:
    for test_id, _ in format["url"].items():
        extract_test(format["tests_format"], test_id)