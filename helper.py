import random
import time
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse
import requests

other_website=['https://quora.com','https://twitter.com','https://www.reddit.com','https://www.tumblr.com']

def write_output_to_file(output_file_path, input_file_path, processed_lines):
    print("Writing output")
  
   
    # Write processed lines to the output file
    with open(output_file_path, 'a') as output_file:
        output_file.writelines(processed_lines)

    # Remove the processed lines from the input file
    with open(input_file_path, 'r') as input_file:
        remaining_lines = input_file.readlines()[len(processed_lines):]
    

    with open(input_file_path, 'w') as input_file:
        input_file.writelines(remaining_lines)

def randomness_generator(driver):
    scroll_iterations = random.randint(3, 5)
   
    wait_time = random.randint(1, 3)
    
    for _ in range(scroll_iterations):
         # Generate a random choice between Keys.PAGE_DOWN and Keys.PAGE_UP
        scroll_action = random.choice([Keys.PAGE_DOWN, Keys.PAGE_UP])
        driver.find_element(By.TAG_NAME, 'body').send_keys(scroll_action)
        # Adjust the sleep time as needed (e.g., 1 second for a slower scroll)
        time.sleep(wait_time)  

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

def visit_other_site(driver):
    time.sleep(random.randint(2,5))
    driver.get(random.choice(other_website))
    time.sleep(random.randint(2,5))
    

def download_image(url, directory, file_name):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            if not os.path.exists(directory):
                os.makedirs(directory)
            file_path = os.path.join(directory, file_name)
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"Image downloaded: {file_name}")
        else:
            print(f"Failed to download image from {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading image from {url}: {str(e)}")