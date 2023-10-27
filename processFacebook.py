import time
from selenium.webdriver.common.by import By
import helper
import random 
import processVideo
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs
from selenium.common.exceptions import TimeoutException  # Import TimeoutException

def attempt_facebook_login(input_username, input_password, browser):
    print(input_username, input_password)
    browser.get('https://www.facebook.com')
    username = browser.find_element(By.ID,"email")
    password = browser.find_element(By.ID,"pass")
    submit   = browser.find_element(By.NAME,"login")
    username.send_keys(input_username)
    password.send_keys(input_password)
    submit.click()
    time.sleep(5)
    current_url = browser.current_url

    # Parse the current URL to extract query parameters
    parsed_url = urlparse(current_url)
    query_params = parse_qs(parsed_url.query)
    

    key = ''
    value = ''
    for key, values in query_params.items():
        key = key
        value = values[0]
    if(key == 'sk' and value == 'welcome'):
        with open('facebook_cookies.txt', 'w') as cookie_file:
            for cookie in browser.get_cookies():
                cookie_file.write(f"{cookie['name']}={cookie['value']}\n")


#To attempt cookie login, you need to attemp facebook login first. It will create a file facebook_cookies.txt which needs to be passed as url in this function.
def attempt_cookie_login_facebook(url, browser):
    browser.get('https://www.facebook.com')

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

    # Browse back to facebook 
    browser.get('https://www.facebook.com')

    time.sleep(random.randint(8,15))
    
def perform_facebook_action(driver,data, downloader_fn, randomness_fn, line):
    try:
        error = ''
        driver.get(data['postUrl'])
        try:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'userContent')]")))
        except TimeoutException:
            element = None
            print("No Caption found")

        
        if(data['type'] == 'native_video' or data['type']== 'live_video_complete' ):
            error = processVideo.downloadVideo(driver,data['postUrl'], data['platformId'])
            get_text_from_facebook(element, data['platformId'], f"./videos/{data['platformId']}.final.mp4")

        elif(data['type'] == 'video' or data['type'] == 'youtube'):
            for d in data['media']:
                if(d['type'] == 'video'):
                    youtube = 0
                    if(data['type'] == 'youtube'):
                        youtube= 1
                    processVideo.downloadVideo(driver,d['url'],data['platformId'] , youtube)
                    get_text_from_facebook(element, data['platformId'], f"./videos/{data['platformId']}.final.mp4")
     
        else:
            error = downloader_fn(driver, data['platformId'], element)
        randomness_fn(driver)
        time.sleep(random.randint(3,7))
        return error
    except json.JSONDecodeError as e:
        print(f"Error processing line: {line.strip()}")
        raise e

def get_images_from_facebook_not_logged_in(driver, filename, caption_element):
    try:
        elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//img[contains(@class, 'scaledImageFitWidth')]")))

        src = elements[1].get_attribute("src")
        if(src):
            file_name = helper.convert_to_jpg(filename)
            helper.download_image(src, 'facebook', file_name )
            get_text_from_facebook(caption_element, filename, f'./facebook/{file_name}')
        else:
            return "Not Found"
        

    except Exception as e:
        print(f'Error: Unable to download the image {str(e)}')
        raise e

def get_text_from_facebook(element, filename, file_name):
    text = ""
    
    p_tags = []
    
    if(element != None):
        p_tags = element.find_elements(By.TAG_NAME, 'p')
    if(p_tags and len(p_tags) > 0):
        for p_tag in p_tags:
            text += p_tag.text + "\n"
               
    data = {f'{filename}' : text, "path" : f'{file_name}'}
    json_data = json.dumps(data, indent=4)
    with open('./facebook_data.jsonl', 'a') as file:
        file.write(json_data + "\n")
    

    
def get_images_from_facebook(driver, filename):
    try:
        elements = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='x10l6tqk x13vifvy']")))
        img_element = elements.find_element(By.TAG_NAME, "img")
        src = img_element.get_attribute("src")
        file_name = helper.convert_to_jpg(filename)
        helper.download_image(src, 'facebook', file_name )

    except Exception as e:
        print(f'Error: Unable to download the image {str(e)}')
        raise e