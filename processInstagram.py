
import time
from selenium.webdriver.common.by import By
import helper
import random 
import processVideo
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def attempt_instagram_login(user_name, user_pass, browser):
    browser.get('https://www.instagram.com')
    time.sleep(5)
    username = browser.find_element(By.NAME,"username")
    password = browser.find_element(By.NAME,"password")
    submit   = browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    username.send_keys(user_name)
    password.send_keys(user_pass)
    submit.click()
    time.sleep(10)

    with open('instagram_cookies.txt', 'w') as cookie_file:
        for cookie in browser.get_cookies():
            cookie_file.write(f"{cookie['name']}={cookie['value']}\n")


def attempt_cookie_login_instagram(url, browser):
    browser.get('https://www.instagram.com')

    with open(url, 'r') as cookie_file:
        for line in cookie_file.readlines():
            cookie_data = line.strip().split('=')
            if len(cookie_data) == 2:
                cookie = {
                    'name': cookie_data[0],
                    'value': cookie_data[1],

                }
                # print(cookie)
                browser.add_cookie(cookie)

    helper.visit_other_site()

    # Browse back to instagram 

    browser.get('https://www.instagram.com')

    time.sleep(random.randint(8,15))

def perform_instagram_action(driver,data, downloader_fn, randomness_fn, line):
    try: 
        if(data['type'] == 'video'):
            processVideo.downloadVideo(driver,data['postUrl'], str(int(time.time())))
        else:
            driver.get(data['postUrl'])
            downloader_fn(driver)
        randomness_fn(driver)
        time.sleep(random.randint(3,7))
    except json.JSONDecodeError as e:
        print(f"Error processing line: {line.strip()}")

def get_images_from_instagram(driver):
    wait = WebDriverWait(driver, 15)  # Adjust the timeout (in seconds) as needed
    try:
        # Use expected_conditions to wait for the element with class "_aagv" to appear
        elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='x1i10hfl']//div[@class='_aagu']//div[@class='_aagv']")))

        for element in elements:
            img_element = element.find_element(By.TAG_NAME, "img")           
            src = img_element.get_attribute("src")
            
            if src:
                file_name = helper.get_file_name_from_imagesrc(src)
                helper.download_image(src,'instagram',file_name)
                
    except Exception as e:
        print(f'Error: {str(e)}')   



