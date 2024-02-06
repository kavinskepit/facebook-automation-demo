import os
import shutil
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import TimeoutException
import openai
import facebook
from selenium.webdriver.chrome.options import Options
import requests
from openai import OpenAI
from monsterapi import client
import schedule
import threading
from datetime import datetime, timedelta
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
import pytz 
from datetime import datetime, timezone
import os
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import tempfile
from pymongo import MongoClient
from bs4 import BeautifulSoup
import uuid
import hashlib

OPENAI_API_KEY = "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"
client1 = MongoClient("mongodb+srv://deepak:jLc4IM4dEdJLS7zc@cluster0.qfolmjg.mongodb.net/?retryWrites=true&w=majority")
db = client1["FBautomation"]
collection = db["Data"]
#tes

browser=None
@st.cache_resource(show_spinner=False)        
def get_logpath():
    return os.path.join(os.getcwd(), 'selenium.log')

@st.cache_resource(show_spinner=False)
def get_chromedriver_path():
    return shutil.which('chromedriver')

@st.cache_resource(show_spinner=False)
def get_webdriver_options():
    options = Options() 
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-features=NetworkService")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--disable-notifications")
    return options


def get_webdriver_service(logpath):
    service = Service(
        executable_path=get_chromedriver_path(),
        log_output=logpath,
    )
    return service

def delete_selenium_log(logpath):
    if os.path.exists(logpath):
        os.remove(logpath)

def show_selenium_log(logpath):
    if os.path.exists(logpath):
        with open(logpath) as f:
            content = f.read()
            st.code(body=content, language='log', line_numbers=True)
    else:
        st.warning('No log file found!')

def run_selenium(logpath):
    browser=webdriver.Chrome(options=get_webdriver_options(), service=get_webdriver_service(logpath=logpath))
        
        
    return browser
    
#function to save browser 
def hash_thread_rlock(rlock):
    # You can customize this hash function based on your specific use case
    return hash(str(id(rlock)))

def generate_private_id(username):
    # Generate a unique identifier for the user
    unique_id = str(uuid.uuid4())

    # Combine the unique_id with the username (or any other user-specific data)
    combined_data = unique_id + username

    # Hash the combined_data for privacy
    hashed_id = hashlib.sha256(combined_data.encode()).hexdigest()

    return hashed_id

#function to validate user
@st.cache_data
def validate_user_credentials(username, password):
    # Replace this with your validation logic
    return username == "Skepitglobal" and password == "Skepitglobal"

@st.cache_data
def content_generator(restuarant_name, location, nature_of_cuisine, occasion, offer):
    '''prompt = f"You are a prompt engineering assistant. Create a Facebook post for resturant {restuarant_name} at location {location} and my nature of cuisine is {nature_of_cuisine} for the {occasion} occasion and we are giving flat {offer} discount  and add relevant tags. Generate content without user involvement and limit to 50 words"
    #Generate content for the Facebook post using GPT-3.5 Turbo
    clientopenai = OpenAI(api_key=OPENAI_API_KEY)
    response = clientopenai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a prompt engineering assistant."},
                {"role": "user", "content": prompt},
            ]
        )
            #content=response['choices'][0]['message']['content']
    content= response.choices[0].message.content'''
    content = "tetssfs"
    return content


#function to generate image content for facebok post    
@st.cache_data
def image_generator(other_keywords):
    max_wait_time=300
    api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IjMyYTZhMmFkZDhlMWIyODdjODI1NGM4MmU0OTVjM2UzIiwiY3JlYXRlZF9hdCI6IjIwMjQtMDEtMDRUMDY6MTg6NTQuNjMxODM4In0.LYY0PAaj4F0dj25V2elQaErz8u7pZJITnhL9qAc2lx8'  # Your API key here
    
    monster_client = client(api_key)
    model = 'sdxl-base'
    input_data = {
        'prompt': other_keywords,
        'negprompt': 'unreal, fake, meme, joke, disfigured, poor quality, bad, ugly, text, letters, numbers, humans',
        'samples': 2,
       'steps': 50,
        'aspect_ratio': 'square',
        'guidance_scale': 7.5,
        'seed': 2414,
        }
    result = monster_client.generate(model, input_data)
    image_urls = result['output']
    #image_urls = ["https://www.simplilearn.com/ice9/free_resources_article_thumb/Coca_Cola_Marketing_Strategy_2022.jpg"]
    return image_urls


# Function for Facebook login 
def facebook_login(username, password):
    #global browser
    #chrome_options = ChromeOptions()
    #chrome_options.add_argument("--disable-notifications")
    #chrome_driver_path = "C:\\Users\\srija\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
    #chrome_options = ChromeOptions()
    #service = Service(chrome_driver_path)
    #chrome_options.add_argument("--disable-notifications")
    
    #browser = webdriver.Chrome(options=chrome_options)
    #browser = webdriver.Chrome(service=service, options=chrome_options)
    logpath=get_logpath()
    delete_selenium_log(logpath=logpath)
    browser=run_selenium(logpath=logpath)
    
    browser.get("http://www.facebook.com")
    
    username_elem = browser.find_element(By.ID, "email")
    password_elem = browser.find_element(By.ID, "pass")
    button = browser.find_element(By.CSS_SELECTOR, 'button[data-testid="royal_login_button"]')
    
    browser.maximize_window()
    username_elem.send_keys(username)
    password_elem.send_keys(password)
    button.click()

    # Use WebDriverWait to wait for the element to be present and visible
    try:
        element = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/img"))
        )
        if element.is_displayed():
            st.info("Please check for login notifcation in your facebook account and approve the login ")
            #time.sleep(40)
        

            element = WebDriverWait(browser, 120).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[2]/div[4]/div/div[1]"))
                )

                # Once the element is found, you can perform further actions
        #print("Element found:", element.text)
    
        #time.sleep(40)
    except:
        pass
    
    return browser

@st.cache_data                          
def initialize_user_data():
    try:
        user_data = pd.read_excel("user_data.xlsx")
    except FileNotFoundError:
        columns = ['Username', 'Password', 'Appname', 'PageID', 'AccessToken']
        user_data = pd.DataFrame(columns=columns)
        user_data.to_excel("user_data.xlsx", index=False)
    return user_data

@st.cache_data                          
def initialize_user_data2():
    try:
        user_data = pd.read_excel("user_data.xlsx")
    except FileNotFoundError:
        columns = ['Username', 'Password', 'Appname', 'PageID', 'AccessToken']
        user_data = pd.DataFrame(columns=columns)
        user_data.to_excel("user_data.xlsx", index=False)
    return user_data




@st.cache_data
def new_entry_user(username,password,App_name,page_id,access_token):
    user_data = initialize_user_data()
    new_entry = pd.DataFrame([[username, password, App_name, page_id, access_token]],
                columns=['Username', 'Password', 'Appname', 'PageID', 'AccessToken'])
    user_data = pd.concat([user_data, new_entry], ignore_index=True)
    user_data.to_excel("user_data.xlsx", index=False)
    
#function to post scheduled post of a generated image                                    
@st.cache_data
def post_to_facebook_demo_schedule_image_url(access_token, page_id, message, image_path, scheduled_datetime, selected_timezone):
    graph = facebook.GraphAPI(access_token)

    # Convert scheduled_datetime to the selected timezone
    scheduled_datetime = pytz.timezone(selected_timezone).localize(scheduled_datetime)

    # Convert scheduled_datetime to Unix timestamp (number)
    scheduled_timestamp = int(scheduled_datetime.timestamp())

    # Schedule the post
    
    graph.put_photo(parent_object=page_id, image=image_path, message=message, published=False, scheduled_publish_time=scheduled_timestamp)
    
    
        

# Function for profile and page retrieval
#@st.cache_data(hash_funcs={_thread.RLock: hash_thread_rlock})
def retrieve_profiles_and_pages(browser):
    facebook_button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div[1]/a')))
    facebook_button.click()
    time.sleep(2)
    
    try:
        outer_profile_element = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".x14yjl9h.xudhj91.x18nykt9.xww2gxu.x10l6tqk.xhtitgo"))
        )
        outer_profile_element.click()
        time.sleep(4)
            
        inner_profile_element = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x1ypdohk.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1o1ewxj.x3x9cwd.x1e5q0jg.x13rtm0m.x87ps6o.x1lku1pv.x1a2a7pz.x9f619.x3nfvp2.xdt5ytf.xl56j7k.x1n2onr6.xh8yej3'))
        )
        inner_profile_element.click()
        time.sleep(4)
    except:
        outer_profile_element = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[2]/div[5]/div[1]/span/div"))
            )
        outer_profile_element.click()
        time.sleep(4)
            
        inner_profile_element = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div[5]/div[2]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div[1]/div/div/div[1]/div[1]/div/div/div/div/div/div/div[1]/div[1]/span'))
        )
        inner_profile_element.click()
        time.sleep(4)
        
        
    profile_containers = WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.x1i10hfl.x1qjc9v5.xjbqb8w.xjqpnuy.xa49m3k.xqeqjp1.x2hbi6w.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xdl72j9.x2lah0s.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x2lwn1j.xeuugli.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6.x16tdsg8.x1hl2dhg.xggy1nq.x1ja2u2z.x1t137rt.x1q0g3np.x87ps6o.x1lku1pv.x1a2a7pz.x1lq5wgf.xgqcy7u.x30kzoy.x9jhf4c.x1lliihq[role="radio"]'))
    )
        
    st.write("Profiles and Business pages")
        
    #profile_names = [container.find_element(By.CSS_SELECTOR, '.x1yc453h').text for container in profile_containers]
    #selected_profile = st.selectbox("Select a profile", profile_names)
    #switch_profile(browser, profile_containers, selected_profile)
    return profile_containers



# Function to switch the selected profile
def app_creation(browser, App_name):
    browser.get("https://business.facebook.com/login/?next=https%3A%2F%2Fdevelopers.facebook.com%2F%3Fbiz_login_source%3Dbizweb_unified_login_fb_login_button")
    browser.maximize_window()
    time.sleep(4)
    element_to_click = browser.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[1]/div[2]/div/div[2]/ul/li[5]/a/div[1]")
    element_to_click.click()
                #print("clicked get started button")
                #st.write("clicked get started button")
                
    time.sleep(2)
    try:
        print("clicked register button")
        time.sleep(2)
                    
                    #confirm email button
        confirm_email_button = browser.find_element(By.XPATH, "/html/body/div/div[5]/div[2]/div/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div[3]/div/div[2]")
        confirm_email_button.click()
        print("clicked confirm email button")
        st.write("clicked confirm email button")
        time.sleep(2)
                    
                    #developer radio button
        radio_button_locator = (By.CLASS_NAME, 'x1i10hfl')  # Replace with the actual class name
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable(radio_button_locator))
                    
                    #radio_button = browser.find_element(*radio_button_locator)
                    #radio_button.click()
        try:
            element = browser.find_element(By.CSS_SELECTOR, 'body > div > div:nth-child(11) > div._li._4xit > div > div > div > div > div.x1qjc9v5.x78zum5.x1iyjqo2.xeuugli.xdt5ytf.xs83m0k.xozqiw3.x169t7cy.x2lwn1j > div > div:nth-child(2) > div > div > div > div > div > div > div.x9f619.x78zum5.x1iyjqo2.x5yr21d.x2lwn1j.x1n2onr6.xh8yej3 > div.xw2csxc.x1odjw0f.xwib8y2.xh8yej3 > div.x1iyjqo2.xs83m0k.xdl72j9.x3igimt.xedcshv.x1t2pt76.x1swvt13.x1pi30zi.xexx8yu.x18d9i69 > div._6g3g.xh8yej3 > div > div._6g3g.x1wsuqlk.x5sxuk9 > div > div > div:nth-child(1)')
            element.click() 
            print("clicked dev button 1")
            st.write("clicked dev button 1")
        except:
                element = browser.find_element(By.CSS_SELECTOR, '.x1gzqxud.x1lq5wgf.xgqcy7u.x30kzoy.x9jhf4c.x1bdj1k2.x1y1aw1k.xwib8y2.xurb0ha.x1sxyh0.x78zum5.xdl72j9.xdt5ytf.x2lah0s.x2lwn1j.xeuugli.x1n2onr6.x1afcbsf.x13faqbe.x3oybdh.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x178xt8z.xm81vs4.xso031l.xy80clv.xb9moi8.xfth1om.x21b0me.xmls85d')
                element.click()
                print("clicked dev button 2")
                st.write("clicked dev button 2")
                    
                    
                    #complete registration button
        complete_registration_button = browser.find_element(By.XPATH, "/html/body/div/div[5]/div[2]/div/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div/div[3]/div/div")
        complete_registration_button.click()
        print("clicked complete registration button")
                    
                    #close mark
        try:
            close_button = browser.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[1]/div/div/div/div/div/div[1]/div[2]/div[2]/div/div/div[1]/div[2]/span/div/span/div/div[2]")
            close_button.click()
            print("clicked c button")
            st.write("clicked c button")
        except:
                        #close_button = browser.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[1]/div/div/div/div/div/div[1]/div[2]/div[2]/div/div/div[1]/div[2]/span/div/span/div/div[2]")
                        #close_button.click()
                        #print("clicked c button 2")
                        #st.write("clicked c button")
                print("passed")
        time.sleep(2)
                        
                    #create new app button
        create_newapp = browser.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[2]/div/div/div/div/div/div[1]/div[3]/div[2]/div")
        
                    # Click the element
        create_newapp.click()
        st.write("clicked create_newapp")
        time.sleep(2)
                    
        close_button = browser.find_element(By.XPATH, '//*[@id="facebook"]/body/div[2]/div[1]/div[1]/div/div/div/div/div/div[1]/div[2]/div[2]/div/div/div[3]/div/div')
        
                    # Click the element
        close_button.click()
        st.write("clicked close_button")
                    
                    
                    
    except:
        create_newapp = browser.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[2]/div/div/div/div/div/div[1]/div[3]/div[2]/div/div")
        
        # Click the element
        create_newapp.click()
        #st.write("clicked create_newapp 2 ")
        time.sleep(2)
                    
        try:
            close_button = browser.find_element(By.XPATH, '//*[@id="facebook"]/body/div[2]/div[1]/div[1]/div/div/div/div/div/div[1]/div[2]/div[2]/div/div/div[3]/div/div')
        
        # Click the element
            close_button.click()
            st.write("clicked close_button 2")
        except:
            print("check1")
            
    usecase_button = browser.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[2]/div/div/div/div[3]/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[4]/div")
                # Click the element
    usecase_button.click()
                #time.sleep(4)
        
        
                #click next button
    next_button = browser.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[2]/div/div/div/div[3]/div/div[2]/div/div/div/div[2]/div/div/div")
    next_button.click()
                #time.sleep(4)
        
                #select app type
    apptype_button = browser.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[2]/div/div/div/div/div[3]/div/div[2]/div/div/div/div/div[1]/div[2]/div/div[2]/div/div[2]/div[1]/div")
    apptype_button.click()
                #time.sleep(4)
        
                #close notification
    notification_button = browser.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[3]/div/div/div/div/form/div/div/button")
    notification_button.click()
    time.sleep(4)

                #next button
    next_button = browser.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[2]/div/div/div/div/div[3]/div/div[2]/div/div/div/div/div[1]/div[2]/div/div[3]/div/div")
    next_button.click()
    time.sleep(4)
        
                #type app name
    appname=browser.find_element("xpath", "/html/body/div[1]/div[5]/div[2]/div/div/div/div/div[3]/div/div[2]/div/div/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div/div/div[1]/div[2]/div[1]/div/input")
    appname.send_keys(App_name)
        
                #create app button
    create_app_button = browser.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[2]/div/div/div/div/div[3]/div/div[2]/div/div/div/div/div[1]/div[2]/div/div[4]/div[2]/div[2]/div")
    create_app_button.click()
    time.sleep(4)
        
                #app_event = browser.find_element(By.CSS_SELECTOR, 'a._271k._271m._1qjd._1gwm[href*="/async/products/add/?product_route=analytics"]')
                #app_event.click()
                #time.sleep(6)
        
        
                #link_element = browser.find_element(By.CSS_SELECTOR, 'a.x1i10hfl')
        
                # Click the link
                #link_element.click()
                #time.sleep(4)
        
                #instagram
                #instagram_graph_api_button =  browser.find_element(By.CSS_SELECTOR, 'a._271k._271m._1qjd._1gwm[href*="/async/products/add/?product_route=instagram"]')
        
                #instagram_graph_api_button.click()
                #time.sleep(3)
                #back to product page
                #link_element = browser.find_element(By.CSS_SELECTOR, 'a.x1i10hfl')


                #link_element.click()

                #whatsapp button
                #button_whatsapp = browser.find_element(By.CSS_SELECTOR, 'a._271k._271m._1qjd._1gwm[href*="/async/products/add/?product_route=whatsapp-business"]')
                #button_whatsapp.click()
                #time.sleep(4)

                #back to product page
                #link_element = browser.find_element(By.CSS_SELECTOR, 'a.x1i10hfl')

                #link_element.click()
                #time.sleep(4)
                #business login
                #button_business_login = browser.find_element(By.CSS_SELECTOR, 'a._271k._271m._1qjd._1gwm[href*="/async/products/add/?product_route=business-login"]')
                #button_business_login.click()
                #time.sleep(4)

                #back to product page
                #link_element = browser.find_element(By.CSS_SELECTOR, 'a.x1i10hfl')
                #link_element.click()'

                #tools
    tools_button= browser.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[1]/div/div[1]/div/div/div/div/div/div[2]/a[2]")
    tools_button.click()
    time.sleep(4)

                #graph api explorer
    #graph_api_button = browser.find_element(By.XPATH, '/html/body/div[1]/div[5]/div[2]/div/div/div[2]/div[1]/div[1]')
    graph_api_button = WebDriverWait(browser, 40).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[5]/div[2]/div/div/div[2]/div[1]/div[1]'))
    )   
    graph_api_button.click()
    time.sleep(4)

    

    # Wait for the menu to be present
    button_xpath = '//*[@id="facebook"]/body/div[1]/div[5]/div[2]/div/div[2]/span/div/div[2]/div/div[5]/div[5]/div/div/div/div/div/div[5]/div/button'
    button_element = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, button_xpath))
    )   
    button_element.click()
    print("app button clicked")
    time.sleep(10)



    try:
        try:
            item_xpath = f'//div[contains(., "{App_name}")]/span[@class="_5xzx"]'
            time.sleep(4)

            item_element = WebDriverWait(browser, 40).until(
            EC.element_to_be_clickable((By.XPATH, item_xpath))
            )
                    
            item_element.click()
            time.sleep(2)
        except:
            time.sleep(2)
            xpath_expression = f"//span[contains(@data-tooltip-content, '{App_name}')]"
            element = driver.find_element(By.XPATH, xpath_expression)
            element.click()
            
    except:
        time.sleep(4)
        parent_div = driver.find_element(By.CLASS_NAME, "_7729")

        # Find the child div with specific styles
        child_div = parent_div.find_element(By.CSS_SELECTOR, 'div[style*="background-color: rgb(237, 242, 250); color: rgb(75, 79, 86);"]')
        
        # Find the span element with "afternoon" text
        span_element = child_div.find_element(By.XPATH, './/span[text()="afternoon"]')
        
        # Perform any desired action, for example, click on the element
        span_element.click()
        time.sleep(4)
    
    permissions = browser.find_element(By.XPATH, '/html/body/div[1]/div[5]/div[2]/div/div[2]/span/div/div[2]/div/div[5]/div[5]/div/div/div/div/div/div[9]/div[4]/button')
    permissions.click()

    # Wait for the menu items to be present
    menu_items = WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.uiContextualLayer ul[role="menu"] li a[role="menuitem"]')))
    time.sleep(3)

    # Click on each permissions ans sub permissions
    for item in menu_items:
        item.click()
    time.sleep(4)
        
    elements = WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "_2wpb._3v8w"))
        )

                # Click on each element
    time.sleep(2)
    for element in elements:
        time.sleep(1)
        element.click()
    time.sleep(4)
    permissions.click()


    time.sleep(4)
                #scroll up teh window
    element = browser.find_element(By.XPATH,'/html/body/div[1]/div[5]/div[2]/div/div[2]/span/div/div[2]/div/div[5]/div[5]')
                # Scroll the element into view
    browser.execute_script("window.scrollTo(0, -document.body.scrollHeight);")


    original_window_handle = browser.current_window_handle



                #clicking the generate button
    generate_token_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="facebook"]/body/div[1]/div[5]/div[2]/div/div[2]/span/div/div[2]/div/div[5]/div[5]/div/div/div/div/div/div[2]/div/button'))
        )
    generate_token_button.click() 

    new_window_handle = WebDriverWait(browser, 10).until(EC.number_of_windows_to_be(2))

                # Switch to the new window
    all_window_handles = browser.window_handles
    new_window_handle = [handle for handle in all_window_handles if handle != browser.current_window_handle][0]
    browser.switch_to.window(new_window_handle)
    time.sleep(10)

    button0 = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/form/div/div/div/div/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[2]/div")))
    button0.click()
    time.sleep(2)
            
    try:
        button1 = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/form/div/div/div/div/div/div[2]/div/div[3]/div/label/div/div/div[1]/div/div/div[1]/input")))
        button1.click()
        time.sleep(2)
        
        button2 = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/form/div/div/div/div/div/div[2]/div/div[4]/div/div/div[2]/div[2]/div")))
        button2.click()
        time.sleep(2)
        
        button3 = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/form/div/div/div/div/div/div[2]/div/div[2]/div[2]/div/div/div/label[1]/div/div/div[1]/div/div/div[1]/input")))
        button3.click()
        time.sleep(2)
        
        button4 = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/form/div/div/div/div/div/div[2]/div/div[3]/div/div/div[2]/div[2]/div")))
        button4.click()
        time.sleep(2)
        
        button5 = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/form/div/div/div/div/div/div[2]/div/div[3]/div/div/div[2]/div[2]/div")))
        button5.click()
        time.sleep(2)
        
        button6 = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/form/div/div/div/div/div/div[2]/div/div[3]/div/label/div/div/div[1]/div/div/div[1]/input")))
        button6.click()
        time.sleep(2)
        
        button7 = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/form/div/div/div/div/div/div[2]/div/div[4]/div/div/div[2]/div[2]/div")))
        button7.click()
        time.sleep(2)
        
        button8 = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/form/div/div/div/div/div/div[2]/div/div[4]/div/div/div[2]/div[2]/div")))
        button8.click()
        time.sleep(2)
        
        button9 = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/form/div/div/div/div/div/div[2]/div/div[2]/div/div/div[2]/div/div")))
        button9.click()
        time.sleep(2)
        
        
    except:
        button1 = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/form/div/div/div/div/div/div[2]/div/div[2]/div[2]/div/div/div/label[1]")))
        button1.click()
        time.sleep(2)
        
        button2 = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/form/div/div/div/div/div/div[2]/div/div[3]/div/div/div[2]/div[2]/div")))
        button2.click()
        time.sleep(2)
        
        button3 = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/form/div/div/div/div/div/div[2]/div/div[2]/div[2]/div/div/div/label[1]")))
        button3.click()
        time.sleep(2)
        
        button4 = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/form/div/div/div/div/div/div[2]/div/div[3]/div/div/div[2]/div[2]/div")))
        button4.click()
        time.sleep(2)
        
        button5 = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/form/div/div/div/div/div/div[2]/div/div[2]/div[2]/div/div/div/label[1]")))
        button5.click()
        time.sleep(2)
        
        button6 = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/form/div/div/div/div/div/div[2]/div/div[3]/div/div/div[2]/div[2]/div")))
        button6.click()
        time.sleep(2)
        
        button7 = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/form/div/div/div/div/div/div[2]/div/div[2]/div[2]/div/div/div/label[1]")))
        button7.click()
        time.sleep(2)
        
        button8 = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/form/div/div/div/div/div/div[2]/div/div[3]/div/div/div[2]/div[2]/div")))
        button8.click()
        time.sleep(2)
        
        button9 = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/form/div/div/div/div/div/div[2]/div/div[4]/div/div/div[2]/div[2]/div")))
        button9.click()
        time.sleep(2)
        
        button10 = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/form/div/div/div/div/div/div[2]/div/div[2]/div/div/div[2]/div/div")))
        button10.click()
        time.sleep(2)
                    

    browser.switch_to.window(original_window_handle)
    print("original window")


    access_token = browser.find_element(By.XPATH,"/html/body/div[1]/div[5]/div[2]/div/div[2]/span/div/div[2]/div/div[5]/div[5]/div/div/div/div/div/div[2]/div/div/div[1]/label/input")
                #access token
    value = access_token.get_attribute("value")
                #value="EAAKfwS1Vv6cBOwLlyyhgbTcsoXO2fPdqAEXUQ9O6UgPWRj1bkoZCkNy8wGCPsZADyX6fPQOZAb8gR1T9G8zIPyz9fsNJrGughQtSd4IZBg9L1WbI0ZBAv8ZB15aWnZBvu3tU6B1heTYUuf1R9w52DuL43mozw4HsMb9NaR3ruiP9nGcZCEaqx3k883NjtiAeCt55kCOQLtfuIMSf9gLh434Ru2SGuSJndqUKd2MZD"
                #st.write(f"Retrieved temporary access token : {value}")
                
                #tools button
    tools_button = browser.find_element(By.XPATH, '/html/body/div[1]/div[5]/div[1]/div[2]/div/div/div/div/div/div/div[2]/a[2]')
    tools_button.click()
                
                # access_token_tool_button
    access_token_tool_button = browser.find_element(By.XPATH, '/html/body/div[1]/div[5]/div[2]/div/div/div[2]/div[2]/div[1]/a[1]')
    access_token_tool_button.click()
                
    time.sleep(4)
                
    html_content = browser.page_source
    print(html_content)
    soup = BeautifulSoup(html_content, 'html.parser')

                # Find the div containing the specified text
    desired_div = soup.find('div', class_='_5k-5 _c24 _2iem _50f7', text=App_name)

    if desired_div:
                    # Extract the access token from the corresponding <a> tag
        paccess_token = desired_div.find_next('a')['href'].split('=')[-1]
        print(f"Access Token: {paccess_token}")
                    #st.write("permanatn acces stoken : "+ str(paccess_token))

                #fetching app scoped id
        app_scoped_user_id=""
                    
                # Construct the URL for the /me endpoint
        url = "https://graph.facebook.com/v12.0/me"

                # Prepare parameters
        params = {
                    "access_token": str(value)
                }

        try:
                # Make the request using the requests library
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an HTTPError for bad responses

                    # Parse the JSON response
            data = response.json()

                    # Check for errors
            if "id" in data:
                app_scoped_user_id = data["id"]
                    #return app_scoped_user_id
            else:
                print("Error: User ID not found in the response.")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

                # Get the App-Scoped User ID
        print(app_scoped_user_id)
                
                #st.write(f"Retrieved app_scoped_user_id: {app_scoped_user_id}")
                
        permanant_access_token =""
        url = f"https://graph.facebook.com/v12.0/{app_scoped_user_id}/accounts"

                # Prepare parameters
        params = {
                "access_token": paccess_token
            }

        try:
                        # Make the GET request using the requests library
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an HTTPError for bad responses

                    # Parse the JSON response
            data = response.json()
            pages = []
            
            for item in data.get('data', []):
                page = {
                    'pageName': item.get('name'),
                    'pageId': item.get('id'),
                    'pageAccessToken': item.get('access_token')
                    }
                pages.append(page)
            #user_data = {'pages': pages}
            
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

                #st.write(f"Retrieved  permanant Access token : {permanant_access_token}")
            
        
        access_token = permanant_access_token
        browser.close()
                #st.write(f"Retrieved permanant Access token ID: {access_token}")
        return pages,access_token

#function to upload file to the streamlit app
@st.cache_data
def save_uploaded_file(uploaded_file):
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue())
    return file_path 
        
#function to post the uploaded file by the user
@st.cache_data        
def post_to_facebook_demo_file_upload(access_token, page_id, message, image_path):
    graph = facebook.GraphAPI(access_token)
    print(page_id)
    graph.put_photo(parent_object='me', image=open(image_path, 'rb'), message=message)
    st.text ("Posted")  
@st.cache_data
#posting to facebook page
def post_to_facebook_demo(access_token, page_id, message, image_path):
    image_url = image_path
    image_response = requests.get(image_url)
    graph = facebook.GraphAPI(access_token)
    print(page_id)

    # Check if the request was successful (status code 200)
    if image_response.status_code == 200:
    # Open the image file in binary mode
        with open('local_image.png', 'wb') as file:
            # Write the content of the response to the file
            file.write(image_response.content)

            # Now you can use 'local_image.png' as the image path in your code
        graph.put_photo(parent_object='me', image=image_response.content, message=message)
        # image=open(image_path, 'rb'),
        st.text ("Posted")

    else:
        print(f"Failed to download image. Status code: {image_response.status_code}")
        
@st.cache_data       
def post_to_facebook_demo_schedule_file_upload(access_token, page_id, message, image_path, scheduled_datetime, selected_timezone):
    graph = facebook.GraphAPI(access_token)

    # Convert scheduled_datetime to the selected timezone
    scheduled_datetime = pytz.timezone(selected_timezone).localize(scheduled_datetime)

    # Convert scheduled_datetime to Unix timestamp (number)
    scheduled_timestamp = int(scheduled_datetime.timestamp())

    # Schedule the post
    
    graph.put_photo(parent_object=page_id, image=open(image_path, 'rb'), message=message, published=False, scheduled_publish_time=scheduled_timestamp)
    
                    

@st.cache_resource(show_spinner=False, experimental_allow_widgets=True)
def insert_data(App_name, private_id, pages):
    user_data = {"App_name": App_name, "private_id": private_id, "pages": pages}
    collection.insert_one(user_data)
    st.success("Data saved successfully.")

# Main Streamlit app
def main():
    st.title("Welcome to Facebook Post Automation App")
    
    if 'browser' not in st.session_state:
        st.session_state.browser = None
    
    # Sidebar dropdown for login options
    login_option = st.sidebar.selectbox("Choose login option:", ("Select", "Admin login", "User login"))

    if login_option == "Select":
        st.warning("Please select a login option.")

    elif login_option == "Admin login":
        st.warning("Admin login feature is not implemented yet.")
        # You can add admin login functionality here if needed.

    elif login_option == "User login":
        # User credentials step
        if st.checkbox('Existing user'):
            st.header("Login")
            unique_id = st.text_input("Enter you unique id:",key="unique_id", placeholder="Enter the unique Id provided to you during new user registration ")
            data = collection.find_one({"private_id": unique_id})
            if data:
                pages = data.get("pages", [])
                selected_page = st.selectbox("Select Page", [page["pageName"] for page in pages])
                # Retrieve page details based on the selected page
                selected_page_data = next((page for page in pages if page["pageName"] == selected_page), None)
                if st.checkbox("Login"):
                    if selected_page_data:
                        #st.write(f"Page ID: {selected_page_data['pageId']}")
                        #st.write(f"Page Access Token: {selected_page_data['pageAccessToken']}")
                        page_id =selected_page_data['pageId']
                        access_token = selected_page_data['pageAccessToken']
                        # Facebook login and profile selection step
                        st.subheader("Content generation form")
                        #App_name = st.text_input("Enter your Facebook App Name        (the app name must be more than 5 letters and not start with the letter fb)")
                        restuarant_name=st.text_input("Enter Your Business name",key="Resturant_existing_user")
                        nature_of_cuisine=st.text_input("Enter Nature of Cuisine",key="Cuisine_existing_user")
                        occasion=st.text_input("Enter the occasion",key="occasion_existing_user")
                        offer=st.text_input("Enter the offer or the discount",key="discount_existing_user")
                        other_keywords=st.text_input("Enter keywords to describe the image / poster you want to post",key="poster_existing_user", placeholder="Give description to generative the image")
                        location=st.text_input("Enter your location",key="location_existing_user")
                        if st.checkbox("Run",key="Run_existing_user"):
                            st.subheader("Facebook Post Content Generation")
                            content=content_generator(restuarant_name,location,nature_of_cuisine,occasion,offer)
                            modified_content=st.text_area("Generated Facebook Post Content",content,key="modified_content_existing_user")
                            #image generation
                            image_urls= image_generator(other_keywords)
                            for i, image_url in enumerate(image_urls):
                                st.image(image_url, caption=f'Image {i + 1}', use_column_width=True, width=200)
                            selected_image_index = st.text_input("Enter the image you want to choose (choose integers)")
                            #upload image
                            uploaded_file = st.file_uploader("Choose an image file to upload", type=["jpg", "jpeg", "png"],key="uploaded_file_existing_user")
                            
                            if st.checkbox("Click here to post to fb account"):    
                                if selected_image_index:
                                    st.write("Posting images")
                                    if 1 <= int(selected_image_index) <= len(image_urls):
                                        st.session_state.selected_image_index = int(selected_image_index) - 1
                                        st.session_state.selected_image_url = image_urls[int(selected_image_index) - 1]
                                        image_path= image_urls[int(selected_image_index) - 1]
                                        st.text(f"Selected Image {selected_image_index}")  
                                                            
                                        message = str(modified_content)

                                        if st.checkbox("Schedule the facebook Post",key="Schedule_Post_existing user"):
                                            image_url = image_path
                                            image_response = requests.get(image_url)
                                                    # graph = facebook.GraphAPI(access_token)
                                            print(page_id)
                                            image_path = image_response.content
                                                                        
                                            caption = modified_content
                                                                        # Replace with your User Access Token, Page ID, and desired API version
                                                    #user_access_token = access_token
                                                                        

                                                    #api_version = "v13.0"

                                                                        # Make a request to get the Page Access Token
                                                    #url = f"https://graph.facebook.com/{api_version}/{page_id}?fields=access_token&access_token={user_access_token}"
                                                    #response = requests.get(url)
                                                    #data = response.json()

                                                                        # Extract the Page Access Token
                                                    #page_access_token = data.get("access_token")
                                                    #print(f"Page Access Token: {page_access_token}")
                                            st.header("Scheduling posts on Facebook")
                                            message = modified_content
                                            scheduled_date = st.date_input("Select date:",key="date_existing user")
                                            scheduled_time = st.time_input("Select time:",key="time_existing user")

                                                                        # Combine date and time to create a datetime object
                                            scheduled_datetime = datetime.combine(scheduled_date, scheduled_time)

                                                                        # Step 8: Display all timezones in a dropdown
                                            timezones = pytz.all_timezones
                                            selected_timezone = st.selectbox("Select timezone:", timezones,key="timezone_existing user")

                                                                        # Step 9: Store the selected timezone
                                            st.write(f"Selected Timezone: {selected_timezone}")

                                                                        # Step 9 & 10: Post the Facebook post according to the date, time, and timezone
                                            if st.button("Schedule Post confirm",key="Postexisting user"):
                                                if  message and scheduled_datetime:
                                                    try:
                                                                                    # Save the uploaded file and get the file path
                                                                                    #image_path = save_uploaded_file(uploaded_file)
                                                        post_to_facebook_demo_schedule_image_url(access_token, page_id, message, image_path, scheduled_datetime, selected_timezone)
                                                        st.success("Post scheduled successfully!")
                                                    except Exception as e:
                                                        st.error(f"Error scheduling post: {e}")
                                                else:
                                                    st.warning("Please fill in all the required fields.")                                
                                        if st.checkbox("Post to facebook account Now"):
                                            post_to_facebook_demo(access_token, page_id, message, image_path)
                                            st.success("Post published successfully.")
                                                                # Button to close the browser 
                                    else:
                                        st.warning(f"Invalid image index. Please enter a number between 1 and {len(image_urls)}.")
                                if uploaded_file:
                                    #facebook_username = st.text_input("Enter your Facebook username")
                                    #facebook_password = st.text_input("Enter your Facebook password", type="password")
                                    image_path = save_uploaded_file(uploaded_file)
                                    if st.checkbox("Login to facebook",key="uploaded_file_Login_existing user"):
                                        st.info("Logging in to Facebook...")
                                        message = str(modified_content)
                                        if st.checkbox("Schedule post",key="uploaded_file_post_existing user"):
                                            print(page_id)
                                            user_access_token = access_token
                                            api_version = "v13.0"
                                                        # Make a request to get the Page Access Token
                                            url = f"https://graph.facebook.com/{api_version}/{page_id}?fields=access_token&access_token={user_access_token}"
                                            response = requests.get(url)
                                            data = response.json()
                                                        # Extract the Page Access Token
                                            page_access_token = data.get("access_token")

                                            print(f"Page Access Token: {page_access_token}")
                                            st.header("Scheduling posts on Facebook")
                                                                    #uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
                                            message = modified_content
                                            scheduled_date = st.date_input("Select date to publish post:")
                                            scheduled_time = st.time_input("Select time to publish post:")
                                                        # Combine date and time to create a datetime object
                                            scheduled_datetime = datetime.combine(scheduled_date, scheduled_time)
                                                        # Step 8: Display all timezones in a dropdown
                                            timezones = pytz.all_timezones
                                            selected_timezone = st.selectbox("Select the timezone :", timezones)
                                                        # Step 9: Store the selected timezone
                                            st.write(f"Selected Timezone: {selected_timezone}")
                                                        # Step 9 & 10: Post the Facebook post according to the date, time, and timezone
                                            if st.button("Schedule the Post"):
                                                if uploaded_file and message and scheduled_datetime:
                                                    try:
                                                        image_path = save_uploaded_file(uploaded_file)
                                                        post_to_facebook_demo_schedule_file_upload(access_token, page_id, message, image_path, scheduled_datetime, selected_timezone)
                                                        st.success("Post scheduled successfully!")
                                                    except Exception as e:
                                                        st.error(f"Error scheduling post: {e}")
                                                else:
                                                    st.warning("Please fill in all the required fields.")
                                        if st.checkbox("Post Now to your page"):
                                            post_to_facebook_demo_file_upload(access_token, page_id, message, image_path)
                                            st.success("Post published successfully.")                                            
                    else:
                        st.warning("Please select a page.")
            else:
                st.warning("No data found for the provided ID.") 
        if st.checkbox('New user'):
            st.subheader("User Credentials")
            user_username = st.text_input("Enter your username")
            user_password = st.text_input("Enter your password", type="password")

            if st.checkbox("Validate User Credentials"):
                if validate_user_credentials(user_username, user_password):
                    st.success("User credentials validated successfully!")
                    st.header("Facebook Login ")
                    facebook_username = st.text_input("Enter Facebook  username")
                    facebook_password = st.text_input("Enter Facebook  password" , type="password")
                    #restaurant_name = st.text_input("Enter restaurant Name")
                    Name = st.text_input("Enter Name")
                    #App_name = restaurant_name
                    App_name = Name
                    
                    if st.checkbox("Login to facebook"):
                        username=facebook_username
                        password=facebook_password
                        if facebook_username and facebook_password:
                            #st.info("Logging in to Facebook...")
                            #login to facebook
                            if st.session_state.browser is None:
                                st.info("Logging in to Facebook...")
                               
                                st.session_state.browser = facebook_login(username, password)
                                st.info("Logged into Facebook ")
                                st.write(" Please click on Retrieve Profiles and Pages")
                            else:
                                st.write("Browser already logged in.")
                        else:
                            st.warning("Please enter both Facebook username and password.")        
                    if st.checkbox("Retrieve Profiles and Pages",key='second'):
                        if st.session_state.browser is not None:     
                            #unique id 
                            #private_id = generate_private_id(username)
                            #st.write(private_id)
                            private_id = generate_private_id(username)
                                            
                                            
                            pages,permanant_access_token = app_creation(st.session_state.browser, App_name)
                            print("token")
                            
                            
                                        
                            access_token = permanant_access_token  # Your Facebook access token here
                                                    #page_id = '179897971873271'  # Your Facebook page ID here
                            #st.write(page_id)
                            #st.write(permanant_access_token)
                                              
                            #new_entry_user(username,password,App_name,page_id,access_token)
                            #print(token)                        
                            #message = str(modified_content)
                            insert_data(App_name, private_id, pages)
                            #permanant_access_token=access_token
                            #page_id = page_id
                            st.write(" Your registration is complete. Click on 'Existing User' to share your content.")
                            st.write("                                                         ")
                            st.write("Please retain this unique code for login purposes:")
                            #private_id = generate_private_id(username)
                            st.markdown(private_id)
                            #st.write("Save this Unique code for logging in ")
                                    
                                            
                        else:
                            st.error("Please log in first.")                        
                else:
                    st.error("Invalid user credentials. Please try again.")
    
# Run the Streamlit app
if __name__ == "__main__":
    main()
