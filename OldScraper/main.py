STARTING_PAGE = 1
DRIVER_LOCATION = "C:/Users/ishannarula/phantomjs/bin"

import time
import requests
import os
import csv
from bs4 import BeautifulSoup
import pandas as pd
import extraction
import output

total_time = 0
start = time.time()
from selenium import webdriver

print()
print("Setting up Chrome webdriver...")

driver = webdriver.Chrome(DRIVER_LOCATION + "/chromedriver")
driver.get("https://www.seedandspark.com/fund/search/all")

end = time.time()
delta = round(end - start, 2)
total_time = total_time + delta

print("Set up driver in " + str(delta) + " seconds")
print()

path_exists = os.path.exists("csv_files")
if (path_exists):
    print("Writing to current 'csv_files' directory...")
else:
    print("Creating new 'csv_files' directory to write to...")
    os.mkdir("csv_files")
print()

# num_pages = 1
num_pages = len(driver.find_elements_by_class_name("pageNum"))
file_names = []

for next_counter in range(STARTING_PAGE - 1):       # indicate to skip to a certain page
    next_button = driver.find_element_by_class_name("pageNext")
    next_button.click()
    time.sleep(0.5)
    total_time = total_time + 0.5

for page_counter in range(STARTING_PAGE - 1, num_pages):

    cards = driver.find_elements_by_css_selector(".card-module.studio-card")
    # num_cards = 2
    num_cards = len(cards)

    for card_counter in range(0, num_cards):
        start = time.time()
        print("Generating card " + str(card_counter + 1) + " on page " + str(page_counter + 1) + "...")

        cards = driver.find_elements_by_css_selector(".card-module.studio-card")
        time.sleep(0.5)
        card = cards[card_counter]

        url = card.get_attribute("href")
        card.click()
        time.sleep(0.5)

        req = requests.get(url)
        data = BeautifulSoup(req.content, "html.parser")
        is_complete = extraction.is_complete(data)
        time.sleep(0.5)

        # obtain data elements
        name = extraction.get_name(data)
        genre = extraction.get_genre(data)
        type = extraction.get_length(data)
        location = extraction.get_location(data);
        story = extraction.get_story(data)
        amounts = extraction.get_amounts(data, is_complete)
        num_supporters = extraction.get_num_supporters(data)
        num_followers = extraction.get_num_followers(data)
        rewards = extraction.get_rewards(data, is_complete)
        wishlist = extraction.get_wishlist(data)

        updates = extraction.get_updates(driver)
        team = extraction.get_team(driver)
        community = extraction.get_supporters_and_dates(driver)

        # generate output
        file_name = output.get_file_path(name)
        file_names.append(output.get_file_name(name))

        data_final = output.polish_elements(name, genre, type, location, amounts, num_supporters, num_followers,
                                            rewards, wishlist, updates, team, community, story)

        df = pd.DataFrame(data_final, dtype=object)
        df.T.to_csv(file_name, index=False, header=False)

        end = time.time()
        delta = round(end - start, 2)
        total_time = total_time + delta

        print("Generated in " + str(delta) + " seconds")
        print()

        refreshes = 4;
        if (is_complete):
            refreshes = 3

        for refresh_counter in range(refreshes):
            driver.back()
            time.sleep(0.5)
            total_time = total_time + 0.5

    # end = time.time()
    if page_counter != num_pages - 1:
        next_button = driver.find_element_by_class_name("pageNext")
        next_button.click()
        time.sleep(0.5)
        total_time = total_time + 0.5

    total_time = round(total_time, 2)
    print("Total time elapsed = " + str(total_time) + " seconds")
    print()

df = pd.DataFrame(file_names, dtype=object)
df.to_csv("file_names.csv", index=False, header=False)

print("Total script ran in " + str(total_time) + " seconds")
