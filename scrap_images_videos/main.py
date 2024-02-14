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
    options.add_argument("--disable-features=NetworkService")
    options.add_argument("--disable-features=PageLifecycle")

   
    options.add_argument("--disable-notifications")
    # options.add_argument(f'--proxy-server={next_proxy}')

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
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"154.6.96.2:3128",
        "user" : "samparking111@gmail.com"  
    },
    {
        "ip" :"38.62.223.234:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"38.62.223.179:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"38.62.223.217:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"38.62.223.68:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"38.62.223.188:3128",
        "user" : "samparking111@gmail.com"  
    },
    {
        "ip" :"154.6.96.114:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"38.62.223.200:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"38.62.223.102:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"38.62.223.52:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"38.62.223.111:3128",
        "user" : "samparking111@gmail.com"  
    },
    {
        "ip" :"154.6.96.100:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"38.62.223.133:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"38.62.223.226:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"38.62.223.31:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"154.6.96.241:3128",
        "user" : "samparking111@gmail.com"  
    },
    {
        "ip" :"154.6.96.92:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"154.6.96.6:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"154.6.96.58:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"38.62.223.46:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"154.6.96.18:3128",
        "user" : "samparking111@gmail.com"  
    },
    {
        "ip" :"154.6.96.79:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"154.6.96.200:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"38.62.223.193:3128",
        "user" : "samparking111@gmail.com"  
    }, 
]

proxy_list_facebook = [
    {
        "ip" :"154.6.96.72:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"154.6.96.2:3128",
        "user" : "samparking111@gmail.com"  
    },
    {
        "ip" :"38.62.223.234:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"38.62.223.179:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"38.62.223.217:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"38.62.223.68:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"38.62.223.188:3128",
        "user" : "samparking111@gmail.com"  
    },
    {
        "ip" :"154.6.96.114:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"38.62.223.200:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"38.62.223.102:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"38.62.223.52:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"38.62.223.111:3128",
        "user" : "samparking111@gmail.com"  
    },
    {
        "ip" :"154.6.96.100:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"38.62.223.133:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"38.62.223.226:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"38.62.223.31:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"154.6.96.241:3128",
        "user" : "samparking111@gmail.com"  
    },
    {
        "ip" :"154.6.96.92:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"154.6.96.6:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"154.6.96.58:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"38.62.223.46:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"154.6.96.18:3128",
        "user" : "samparking111@gmail.com"  
    },
    {
        "ip" :"154.6.96.79:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"154.6.96.200:3128",
        "user" : "samparking111@gmail.com"  
    }, 
    {
        "ip" :"38.62.223.193:3128",
        "user" : "samparking111@gmail.com"  
    }, 
   
]


def init(login_fn, proxy_list, login = 0):
    global driver
    global processed_lines
    get_random_proxy(proxy_list)
    if driver is not None:
        driver.quit()
    driver = initiate_selenium(current_proxy, 0)
    if(login == 1):
        login_fn(current_user,"password",driver)
    time.sleep(10)
    
def rotate_proxy(input_file, output_file, driver, visit_other_site, login_fn , action, randomness_generator, image_fn, output, proxy_list, login = 0, max_lines_to_process = 2500):
    # Set the number of loops before rotating the IP
    loops_before_rotation = 25
    

    # Initialize a counter for loops
    loop_counter = 0
    process_lines = 0
    while True:
        processed_lines = []
        error = ''
        try:
            if(process_lines == max_lines_to_process ):
                break
            if loop_counter > loops_before_rotation:
                get_random_proxy(proxy_list)
                visit_other_site(driver)
                if driver is not None:
                    driver.quit()
                driver = initiate_selenium(current_proxy, 0)
                loop_counter = 0
                if(login == 1):
                    login_fn(current_user,"password",driver)
                time.sleep(5)
            with open(input_file_path, 'r') as file:
                line = file.readline()
                if file.tell() == 0:
                    print("The file is empty.")
                    break
                data = json.loads(line)
                processed_lines.append(line)
                action(driver, data, image_fn, randomness_generator,line )
                output(output_file, input_file, processed_lines)
            loop_counter+=1
            process_lines += 1
            time.sleep(10)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            output(error_file_path, input_file, processed_lines)
            loop_counter += 1
            process_lines += 1
            time.sleep(10)
    print("finished processing")


current_proxy = ''
current_user = ''

driver = None

input_file_path = './covid19-vaccine-facebook-examples.jsonl'
output_file_path = './covid19-vaccine-facebook-examples_bak.jsonl'
error_file_path = './covid19-vaccine-facebook-examples_error.jsonl'
init(processFacebook.attempt_facebook_login, proxy_list_facebook, 0)
rotate_proxy(
    input_file_path, 
    output_file_path, 
    driver,
    helper.visit_other_site, 
    processFacebook.attempt_facebook_login,
    processFacebook.perform_facebook_action,
    helper.randomness_generator,
    processFacebook.get_images_from_facebook_not_logged_in,
    helper.write_output_to_file,
    proxy_list_facebook,
    max_lines_to_process=2500
    )



driver.quit()
            
