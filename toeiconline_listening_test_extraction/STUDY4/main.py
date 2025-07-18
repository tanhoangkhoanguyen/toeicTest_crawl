from bs4 import BeautifulSoup
import os, json


from crawl import crawl_html
from url_store import url_dict
from extract_tools import extract_test, extract_answer


crawl_html()
for key, _ in url_dict.items():
    extract_test(key)
    # extract_answer(key)