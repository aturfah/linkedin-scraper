"""Scraper to pull images from Linkedin."""

from os import makedirs, getcwd
import sys
from os.path import join, exists
from shutil import rmtree

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Set up preliminary folders/path stuff
LINKEDIN_DIR = "photos"

LINKEDIN_USER = "vomit.email.2444@gmail.com"
LINKEDIN_PASS = "password12"

if not exists(LINKEDIN_DIR):
    makedirs(LINKEDIN_DIR)

chromedriver_path = join(getcwd(), "chromedriver.exe")
if not chromedriver_path in sys.path:
    sys.path.append(chromedriver_path)

# Browse without opening window
chrome_options = Options()  
chrome_options.add_argument("--headless")  


# Scrape Pages
MAX_URLS = 10
total_urls = 1

urls_to_try = ["https://www.linkedin.com/in/ali-turfah-66b895b1/"]
image_urls = []
browser = webdriver.Chrome(chromedriver_path)
while urls_to_try and total_urls < MAX_URLS:
    url = urls_to_try[0]

    print(urls_to_try)
    urls_to_try.remove(url)

    browser.get(url)
    try:
        print("Getting Profile Image...")
        # Get page's profile image
        profile_image = browser.find_element_by_class_name("pv-top-card-section__photo")
        image_urls.append(profile_image.value_of_css_property("background-image"))

        total_urls += 1

        other_profiles = browser.find_element_by_class_name("pv-browsemap-section").find_element_by_tag_name("ul").find_elements_by_tag_name("li")

    except Exception:
        print("Exception, couldn't find the image.")
        # Set the URL to retry it
        urls_to_try.append(url)

        # Toggle sign-in form
        signin_toggle = browser.find_element_by_css_selector("p.form-subtext.login")
        signin_toggle = signin_toggle.find_element_by_tag_name("a")

        signin_toggle.click()

        # Fill in sign-in form
        signin_form = browser.find_element_by_class_name("login-form")
        login_email = signin_form.find_element_by_id("login-email")
        login_pass = signin_form.find_element_by_id("login-password")
        login_btn = signin_form.find_element_by_id("login-submit")

        login_email.send_keys(LINKEDIN_USER)
        login_pass.send_keys(LINKEDIN_PASS)

        login_btn.click()

browser.close()
print(image_urls)