"""Scraper to pull images from Linkedin."""
from os import makedirs, getcwd
import sys
from os.path import join, exists
from shutil import rmtree

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import requests


def format_number(number, num_digits=3):
    """
    Format a number with leading zeroes.

    The number will take up at least num_digits digits.
    """
    return str(number).zfill(num_digits)


def write_photo(img_url, filename):
    """Code to write photos from url to file."""
    req = requests.get(img_url, stream=True)
    path = "{}/{}.png".format(LINKEDIN_DIR, filename)
    if req.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in req:
                f.write(chunk)


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
MAX_URLS = 50
total_urls = 1

urls_to_try = ["https://www.linkedin.com/in/ali-turfah-66b895b1/"]


browser = webdriver.Chrome(chromedriver_path)
while urls_to_try and total_urls < MAX_URLS:
    url = urls_to_try[0]
    urls_to_try.remove(url)

    browser.get(url)
    try:
        # Get Other Profiles if we're not over the limit
        other_profiles = browser.find_element_by_class_name(
            "pv-browsemap-section")
        other_profiles = other_profiles.find_element_by_tag_name("ul")
        other_profiles = other_profiles.find_elements_by_tag_name("li")

        for profile_row in other_profiles:
            if total_urls + len(urls_to_try) + len(other_profiles) < MAX_URLS:
                profile_link = profile_row.find_element_by_tag_name(
                    "a").get_attribute("href")
                urls_to_try.append(profile_link)

        print("Getting Profile Image #{}...".format(total_urls))
        # Get page's profile image
        profile_image = browser.find_element_by_class_name(
            "pv-top-card-section__photo")
        try:
            img_url = profile_image.value_of_css_property(
                "background-image").replace('url("', "").replace('")', "")
            if img_url == "https://static.licdn.com/sc/h/djzv59yelk5urv2ujlazfyvrk":
                continue
            write_photo(img_url,  format_number(total_urls, 4))

        except Exception:  # No Profile Picture???
            print("Failed, moving onto next script")
            continue

        total_urls += 1

    except Exception:  # We're on the login page
        print("Exception, couldn't find the image.")
        # Set the URL to retry it
        try:
            # Toggle sign-in form
            signin_toggle = browser.find_element_by_css_selector(
                "p.form-subtext.login")
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

            urls_to_try.append(url)
        except Exception:
            continue

browser.close()
