import time, os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Replace with your Google login credentials
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
GOOGLE_EMAIL = os.getenv("GOOGLE_EMAIL")
GOOGLE_PASSWORD = os.getenv("GOOGLE_PASSWORD")

# Set up browser
options = uc.ChromeOptions()
options.add_argument("--disable-popup-blocking")
driver = uc.Chrome(options=options)

try:
    # Step 1: Go to login page
    driver.get("https://study4.com/login/")
    time.sleep(2)

    # Step 2: Click "Đăng nhập với Google"
    google_login_btn = driver.find_element(By.CSS_SELECTOR, ".g-login-button")
    google_login_btn.click()
    time.sleep(3)

    # Step 3: Switch to Google login window
    driver.switch_to.window(driver.window_handles[-1])

    # Step 4: Enter Google email
    email_input = driver.find_element(By.XPATH, '//input[@type="email"]')
    email_input.send_keys(GOOGLE_EMAIL)
    email_input.send_keys(Keys.ENTER)
    time.sleep(3)

    # Step 5: Enter password
    password_input = driver.find_element(By.XPATH, '//input[@type="password"]')
    password_input.send_keys(GOOGLE_PASSWORD)
    password_input.send_keys(Keys.ENTER)
    time.sleep(20)

    # Step 6: Switch back to main window
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(5)

    # Step 7: Go to the main site (you are now logged in)
    driver.get("https://study4.com/")
    time.sleep(3)

    # ✅ Step 8: Get and save the raw HTML
    html = driver.page_source
    with open("study4_home_after_login.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("✅ HTML content saved to study4_home_after_login.html")

finally:
    driver.quit()