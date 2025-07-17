import time, os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
GOOGLE_EMAIL = os.getenv("GOOGLE_EMAIL")
GOOGLE_PASSWORD = os.getenv("GOOGLE_PASSWORD")

options = uc.ChromeOptions()
options.add_argument("--disable-popup-blocking")
driver = uc.Chrome(options = options)

try:
    driver.get("https://study4.com/login/")
    time.sleep(1)

    google_login_btn = driver.find_element(By.CSS_SELECTOR, ".g-login-button")
    google_login_btn.click()
    time.sleep(1)

    driver.switch_to.window(driver.window_handles[-1])

    email_input = driver.find_element(By.XPATH, '//input[@type="email"]')
    email_input.send_keys(GOOGLE_EMAIL)
    email_input.send_keys(Keys.ENTER)
    time.sleep(3)

    password_input = driver.find_element(By.XPATH, '//input[@type="password"]')
    password_input.send_keys(GOOGLE_PASSWORD)
    password_input.send_keys(Keys.ENTER)
    time.sleep(30)

    driver.switch_to.window(driver.window_handles[0])
    time.sleep(5)

    driver.get("https://study4.com/")
    html = driver.page_source
    with open("raw.html", "w", encoding = "utf-8") as f:
        f.write(html)

    print("HTML content saved to study4_home_after_login.html")

finally:
    driver.quit()