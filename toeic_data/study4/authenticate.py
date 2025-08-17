import time, os, pickle
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


GOOGLE_EMAIL = os.getenv("GOOGLE_EMAIL")
GOOGLE_PASSWORD = os.getenv("GOOGLE_PASSWORD")


def log_in():
    options = uc.ChromeOptions()
    options.add_argument("--disable-popup-blocking")
    driver = uc.Chrome(options = options)
    cookie_file = "toeic_data/study4/cookies.pkl"
    
    driver.get("https://study4.com/")
    time.sleep(1)

    if os.path.exists(cookie_file):
        with open(cookie_file, "rb") as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie)
        driver.get("https://study4.com/")
        time.sleep(1)
    else:
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
        time.sleep(60)

        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)

        with open(cookie_file, "wb") as f:
            pickle.dump(driver.get_cookies(), f)
    
    return driver