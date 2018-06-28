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
    print(url)

    print(urls_to_try)
    urls_to_try.remove(url)

    browser.get(url)
    try:
        # Get Other Profiles if we're not over the limit
        other_profiles = browser.find_element_by_class_name("pv-browsemap-section").find_element_by_tag_name("ul").find_elements_by_tag_name("li")
        if len(image_urls) + total_urls < MAX_URLS:
            for profile_row in other_profiles:
                profile_link = profile_row.find_element_by_tag_name("a").get_attribute("href")
                # profile_link = "https://www.linkedin.com{}".format(profile_link)
                urls_to_try.append(profile_link)

        print("Getting Profile Image...")
        # Get page's profile image
        profile_image = browser.find_element_by_class_name("pv-top-card-section__photo")
        try:
            raw_url = profile_image.value_of_css_property("background-image")
            image_urls.append(raw_url.replace('url("', "").replace('")', ""))
        except Exception: # No Profile Picture
            continue
        total_urls += 1

    except Exception: # We're on the login page
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
