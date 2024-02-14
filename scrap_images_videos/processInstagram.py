
import time
from selenium.webdriver.common.by import By
import helper
import random 
import processVideo
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException  # Import TimeoutException
from selenium.webdriver.common.keys import Keys

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
        error = ''
        driver.get(data['postUrl'])

        try:
            element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//h1[contains(@class, '_aacl _aaco _aacu _aacx _aad7 _aade')]")))
        except TimeoutException:
            element = None
            print("No Caption found")
        if(data['type'] == 'video'):
            error = processVideo.downloadVideo(driver,data['postUrl'], data['platformId'])
            get_text_from_instagram(element, data['platformId'], f"./videos/{data['platformId']}.final.mp4")

        else:
            error = downloader_fn(driver, data['platformId'], element)
        randomness_fn(driver)
        time.sleep(random.randint(3,7))
        return error
    except json.JSONDecodeError as e:
        print(f"Error processing line: {line.strip()}")
        raise e
        
def get_images_from_instagram_not_loggedin(driver, filename, caption_element):
    wait = WebDriverWait(driver, 15)  # Adjust the timeout (in seconds) as needed
    try:
        # Use expected_conditions to wait for the element with class "_aagv" to appear
        elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='_aagu _aato']//div[@class='_aagv']")))
        index = 0
        if(len(elements) <= 0):
            return "Not Found"
        files = []
        for element in elements:
            img_element = element.find_element(By.TAG_NAME, "img") 
            driver.execute_script("arguments[0].setAttribute('loading', 'eager');", img_element)
            src = img_element.get_attribute("src")
            
            if src:
                file_name = helper.convert_to_jpg(f'{filename}_{index}')
                helper.download_image(src,'instagram',file_name)
                files.append(f'./instagram/{file_name}')
                index += 1
            else:
                return "Not Found"
        get_text_from_instagram(caption_element, filename=filename, file_name=files)
                
    except Exception as e:
        print(f'Error: {str(e)}')
        raise e  

def get_images_from_instagram(driver, filename):
    wait = WebDriverWait(driver, 15)  # Adjust the timeout (in seconds) as needed
    try:
        # Use expected_conditions to wait for the element with class "_aagv" to appear
        elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='x1i10hfl']//div[@class='_aagu']//div[@class='_aagv']")))

        for element in elements:
            img_element = element.find_element(By.TAG_NAME, "img")           
            src = img_element.get_attribute("src")
            
            if src:
                file_name = helper.convert_to_jpg(filename)
                helper.download_image(src,'instagram',file_name)
                
    except Exception as e:
        print(f'Error: {str(e)}')   
        raise e

    
def get_text_from_instagram(element, filename, file_name):
    if(element == None):
        text = "No Caption Found"
    else:
        text= element.text
    data = {f'{filename}' : text, "path" : file_name}
    json_data = json.dumps(data, indent=4)
    with open('./instagram_data.jsonl', 'a') as file:
        file.write(json_data + "\n")



