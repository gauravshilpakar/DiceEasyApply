import argparse
import json
import os
from itertools import count
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

import resume
from dice import Dice
from locate import locate_element
from dice import diceObject as dice

dice.resume = os.path.abspath(dice.resume)
SEARCH_URL_WITHOUT_PAGE = f"https://www.dice.com/jobs?q={dice.keywords}&countryCode=US&location={dice.location}&page=%s&pageSize=100&filters.postedDate={dice.postedDate}&filters.employmentType=THIRD_PARTY&filters.easyApply=true&language=en"

# see if any data exists for this user
USER_DATA_PATH = os.path.join("cached_data", f"{dice.username}.json")
completed_jobs = []
if not os.path.exists("cached_data"):
    os.mkdir("cached_data")
if os.path.exists(USER_DATA_PATH):
    with open(USER_DATA_PATH, "r") as file_handle:
        completed_jobs = json.loads(file_handle.read())

# Create webdriver, add user data to persist login and not have to relog
options = webdriver.EdgeOptions()
options.add_experimental_option("detach", True)
options.add_argument("--window-size=800,1200")
options.add_extension(os.path.abspath("adblock.crx"))
if dice.cache_path:
    options.add_argument("user-data-dir=" + dice.cache_path)

driver = webdriver.Edge(options=options)
wait = WebDriverWait(driver, dice.wait_s)

# log in
driver.get("https://www.dice.com/dashboard/login")

try:
    elem = wait.until(EC.presence_of_element_located((By.ID, "email")))
    elem.send_keys(f"{dice.username}\t{dice.password}{Keys.RETURN}")
except Exception as e:
    print(e)
    print("Don't need to log in. Continuing.")

# iterate through pages until there are no links
for page_number in count(1):
    search_url = SEARCH_URL_WITHOUT_PAGE % page_number
    driver.get(search_url)
    try:
        search_cards = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.search-card"))
        )
    except Exception as e:
        print(e)
        print("No jobs found within wait limit.")
        break
    # wait for ribbons to appear (if there are ribbons)
    try:
        ribbons = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.ribbon-inner"))
        )
    except:
        ...
    job_urls = []
    for card in search_cards:
        link = card.find_element(By.CSS_SELECTOR, "a.card-title-link")
        job_id = link.get_attribute("id")
        if job_id in completed_jobs:
            continue
        try:
            ribbon = card.find_element(By.CSS_SELECTOR, "span.ribbon-inner")
            if ribbon.text == "applied":
                continue
        except:
            ...
        job_urls.append((job_id, link.text, link.get_attribute("href")))

    for job_id, job_text, job_url in job_urls:
        print(f"Applying to {job_text}.")
        if any(kw.lower() in job_text.lower() for kw in dice.blacklist):
            print("Blacklisted word found in job title, skipping.")
            continue
        driver.get(job_url)
        try:
            try:
                # Scroll the page to the button's location
                read_full = driver.find_element(
                    By.XPATH, '//*[@id="descriptionToggle"]'
                ).click()
            except Exception as e:
                print("No Read full Desc Button")
                print(e)

            skills_text = driver.find_element(
                By.XPATH, '//*[@id="__next"]/div/main/div[2]/div/article/div[3]/section'
            ).text
            # Generate a resume with SKILLS keywords
            resume.main(skills_text)
            driver.execute_script("window.scrollTo(0, 0);")
            print("sleeping")
            sleep(2)
            print("Updated Resume!")

            apply_container = driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div/main/header/div/div/div[4]/div[2]/apply-button-wc",
            )
            apply_container.click()

            print("sleeping")
            sleep(2)
            print("Clicked on Apply!")

            replace_button = driver.find_element(
                By.XPATH,
                '//*[@id="app"]/div/span/div/main/div[2]/div/div/button',
            )
            replace_button.click()

            sleep(2)
            print("Clicked on Replace!")

            file_input = driver.find_element(
                By.XPATH, '//*[@id="fsp-fileUpload"]'
            ).send_keys(os.path.abspath("./resume/Gaurav Shilpakar - Resume 2023.pdf"))

            upload_button = driver.find_element(
                By.XPATH, "/html/body/div[4]/div/div/div[1]/div/div[3]/div/span[3]"
            ).click()

            print("sleeping")
            sleep(2)
            print("Uploaded new Resume!")

            next_button = driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div[4]/div/div[1]/div/div/span/div/main/div[4]/button[2]/span",
            ).click()

            print("sleeping")
            sleep(2)

            apply_button = driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div[4]/div/div[1]/div/div/span/div/main/div[3]/button[2]/span",
            ).click()
            print("sleeping")
            sleep(2)
            print("APPLIED!")
        except Exception as e:
            print(e)
        completed_jobs.append(job_id)
        with open(USER_DATA_PATH, "w") as file_handle:
            file_handle.write(json.dumps(completed_jobs))
