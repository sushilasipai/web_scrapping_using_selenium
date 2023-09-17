import json
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.parse import urlparse, parse_qs
from selenium.common.exceptions import InvalidCookieDomainException
import requests
import os


def download_image(url, file_name):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_name, 'wb') as file:
                file.write(response.content)
            print(f"Image downloaded: {file_name}")
        else:
            print(f"Failed to download image from {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading image from {url}: {str(e)}")

def attempt_facebook_login(input_username, input_password, browser):
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

# Attempting this will result in facebook disabling the account immediately due to violation of their rules and regulation

#To attempt cookie login, you need to attemp facebook login first. It will create a file facebook_cookies.txt which needs to be passed as url in this function.
def attempt_cookie_login(url, browser):
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

def read_jsonl(path):
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                ex = json.loads(line)
                yield ex

def convert_to_jpg(filename):
    base_name = os.path.splitext(filename)[0]
    return f"{base_name}.jpg"

def get_file_name_from_imagesrc(image_src):
    url_path = urlparse(image_src).path
    file_name = os.path.basename(url_path)
    _, file_extension = os.path.splitext(file_name)
    if not file_extension:
        # If it doesn't have an extension, add the default extension
            file_name += '.jpg'
    return convert_to_jpg(file_name)


def get_facebook_post_images(driver, url):
    driver.get('https://www.facebook.com')

    for line in read_jsonl(url):
        if(line['type'] == 'photo' or line['type'] == 'link'):
            driver.get(line['postUrl'])
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//img[contains(@class, "scaledImageFitWidth")]')))

                # Find the image element using XPath
                image_element = driver.find_element(By.XPATH, '(//img[contains(@class, "scaledImageFitWidth")])[2]')
                
                image_src = image_element.get_attribute('src')

                file_name = get_file_name_from_imagesrc(image_src)
                # Download the file from image source
                download_image(image_src, file_name )
                
            except Exception as e:
                print(f'Error: {str(e)}')


def get_instagram_post_images(driver, url):
    driver.get('https://www.instagram.com')

    for line in read_jsonl(url):
        driver.get(line['postUrl'])
        wait = WebDriverWait(driver, 10)  # Adjust the timeout (in seconds) as needed

        
        try:
            # Use expected_conditions to wait for the element with class "_aagv" to appear
            elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, '_aagu') and contains(@class, '_aato') and .//div[contains(@class, '_aagv')]]")))

            for element in elements:
                img_element = element.find_element(By.TAG_NAME, "img")
                
                src = img_element.get_attribute("src")
            
                if src:
                    file_name = get_file_name_from_imagesrc(src)
                    download_image(src,file_name)
            
            # download_all_post_images(img_element)
                
        except Exception as e:
            print(f'Error: {str(e)}')
    


# Create a new Selenium WebDriver instance
chrome_options = webdriver.ChromeOptions()

chrome_options.add_argument("--disable-notifications")

driver = webdriver.Chrome(options=chrome_options)

driver.delete_all_cookies()

#function call to download instagram images
#get_instagram_post_images(driver,"./covid19-vaccine-instagram-examples.jsonl")

#facebook login
attempt_facebook_login("username","password",driver)

#function call to download facebook images
#get_facebook_post_images(driver,"./covid19-vaccine-facebook-examples.jsonl")
        

driver.quit()


