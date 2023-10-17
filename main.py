import json
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import random
import processFacebook
import processInstagram
import helper



def get_random_proxy(proxy_list):
    global current_proxy  # Use the global keyword to modify the outer variable
    global current_user
    proxy = random.choice(proxy_list) 
    if(current_proxy != '' or current_proxy != proxy["ip"]):
        current_proxy = proxy["ip"]
        current_user = proxy["user"]
        print(current_proxy, current_user)
        return current_proxy
    get_random_proxy(proxy_list)


def initiate_selenium(next_proxy, headless = 1):
    # Create a new Selenium WebDriver instance
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

    options = webdriver.ChromeOptions()

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("start-maximized")
    options.add_argument("--autoplay-policy=no-user-gesture-required")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_experimental_option("w3c", desired_capabilities)
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    options.add_experimental_option("useAutomationExtension", False) 

   
    options.add_argument("--disable-notifications")
    options.add_argument(f'--proxy-server={next_proxy}')

    if(headless == 1):
        options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.delete_all_cookies() 
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
    return driver

# Get Proxy IP addresses and 
# put it here along with the user associated with that IP
#You can buy some at https://proxyscrape.com/
proxy_list_instagram = [
    {
        "ip" :"154.6.96.72:3128",
        "user" : "munakellers"  
    },
    {
        "ip" :  "154.6.96.2:3128",
        "user" : "leo.taken13"
    }
    
    # "38.62.223.179:3128",
    # "38.62.223.217:3128",
    # "38.62.223.68:3128",
    # "38.62.223.188:3128",
    # "154.6.96.114:3128",
    # "38.62.223.200:3128",
    # "38.62.223.102:3128",
    # "38.62.223.52:3128",
    # "38.62.223.111:3128"
    # Add more proxy servers as needed
]

proxy_list_facebook = [
    {
        "ip" :"154.6.96.72:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    # {
    #     "ip" : "38.62.223.234:3128",
    #     "user" : "sampark.hehe"
    # }, 
    # {
    #     "ip" :  "154.6.96.2:3128",
    #     "user" : "bakerleo905@gmail.com"
    # }
    
    # "38.62.223.179:3128",
    # "38.62.223.217:3128",
    # "38.62.223.68:3128",
    # "38.62.223.188:3128",
    # "154.6.96.114:3128",
    # "38.62.223.200:3128",
    # "38.62.223.102:3128",
    # "38.62.223.52:3128",
    # "38.62.223.111:3128"
    # Add more proxy servers as needed
]


def init(login_fn, proxy_list):
    global driver
    global processed_lines
    get_random_proxy(proxy_list)
    if driver is not None:
        driver.quit()
    driver = initiate_selenium(current_proxy, 0)
    print(current_user)
    login_fn(current_user,"password",driver)
    time.sleep(10)
    
def rotate_proxy(input_file, output_file, driver, visit_other_site, login_fn , action, randomness_generator, image_fn, output, proxy_list):
    # Set the number of loops before rotating the IP
    loops_before_rotation = 10

    # Initialize a counter for loops
    loop_counter = 0
    while True:
        processed_lines = []
        try:
            if loop_counter > loops_before_rotation:
                get_random_proxy(proxy_list)
                visit_other_site(driver)
                if driver is not None:
                    driver.quit()
                driver = initiate_selenium(current_proxy, 0)
                loop_counter = 0
                login_fn(current_user,"password",driver)
                time.sleep(5)
            with open(input_file_path, 'r') as file:
                line = file.readline()
                if file.tell() == 0:
                    print("The file is empty.")
                    break
                data = json.loads(line)
                action(driver, data, image_fn, randomness_generator,line )
                processed_lines.append(line)  
            
            output(output_file, input_file, processed_lines)
            loop_counter+=1
        except Exception as e:
            print(f"An error occurred: {str(e)}")
    print("finished processing")


current_proxy = ''
current_user = ''

driver = None

input_file_path = './covid19-vaccine-instagram-examples.jsonl'
output_file_path = './covid19-vaccine-instagram-examples_bak.jsonl'

init(processInstagram.attempt_instagram_login, proxy_list_instagram)
rotate_proxy(
    input_file_path, 
    output_file_path, 
    driver,
    helper.visit_other_site, 
    processInstagram.attempt_instagram_login,
    processInstagram.perform_instagram_action,
    helper.randomness_generator,
    processInstagram.get_images_from_instagram,
    helper.write_output_to_file,
    proxy_list_instagram
    )

driver.quit()
            
