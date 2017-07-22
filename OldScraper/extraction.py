import time

# BeautifulSoup data extraction

def is_complete(data):
    return bool(data.find_all("h2", {"class": "greenlight"}))

def get_name(data):
    name = data.find_all("h2", {"class": "project-title"})[0].text
    return name

def get_genre(data):
    genre = data.find_all("h5", {"class" : "genre"})[0].text
    genre = genre.strip().split(",");

    if (len(genre) == 2):
        len_second = len(genre[1])
        genre[1] = genre[1][1:len_second]          # get rid of comma after first element
    return genre

def get_length(data):
    length = data.find_all("h5", {"class" : "length"})[0].text
    return length

def get_location(data):
    location = data.find_all("h5", {"class" : "location"})[0].text
    return location

def get_story(data):
    story = data.find_all("div", {"class": "story-body"})[0].text
    return story

def get_amounts(data, is_complete):
    money = data.find_all("h3", {"class" : "financial"})[0].text
    money = money.split();

    if is_complete:
        amount_target = "N/A";          # green light campaigns don't have target amount
        amount_raised = money[1];
    else:
        amount_target = money[2];
        amount_raised = money[0];

    return [amount_raised, amount_target]

def get_num_supporters(data):
    num_supporters = data.find_all("h3", {"class" : "supporters"})[0].text
    num_supporters = num_supporters.split()[0];
    return num_supporters

def get_num_followers(data):
    num_followers = data.find_all("h3", {"class" : "supporters"})[1].text
    num_followers = num_followers.split()[0];
    return num_followers

def get_rewards(data, is_complete):
    reward_amounts = []
    reward_categories = []

    incentive_items = data.find_all("div", {"class" : "incentive-item"})
    size = int(len(incentive_items) / 2)        # getting rid of duplicate entries
    incentive_items = incentive_items[0:size]

    general = data.find_all("h3")
    start = 7
    if is_complete:     # offset index for green light campaigns
        start = 9

    for item in incentive_items:
        amount = item.find_all("h2")[1].text
        reward_amounts.append(amount)

    remaining_items = len(general) - start;         # check to make sure headers actually exist
    if (size <= remaining_items):
        for counter in range(start, (start + size)):        # grab headers within a certain range
            award = general[counter].getText();
            reward_categories.append(award)
    else:
        for counter in range(size):
            reward_categories.append("N/A")

    return [reward_amounts, reward_categories]

def get_wishlist(data):
    wishlist_items = []
    wishlist_progress = []
    wishlist = data.find_all("div", {"class" : "card-module wishlist-card"})

    for item in wishlist:
        name = item.find_all("p", {"class" : "item-title"})[0].text
        wishlist_items.append(name)

        progress = item.find_all("div", {"class", "card-panel progress"})[0].text
        progress = progress.split()
        remaining_cost = progress[0]

        if remaining_cost == "FULFILLED":
            wishlist_progress.append(100.0)
        else:
            total_cost = convert_money(progress[4])

            if (total_cost != 0):
                remaining_cost = convert_money(remaining_cost)
                difference = total_cost - remaining_cost
                percent = round(difference / total_cost * 100, 1)
                wishlist_progress.append(str(percent) + " %")
            else:
                wishlist_progress.append("100.0 %")

    return [wishlist_items, wishlist_progress]


# Selenium data extraction

def get_updates(driver):
    update_button = driver.find_element_by_xpath("""//*[@id="tab_updates"]""")
    update_button.click()
    time.sleep(0.5)

    update_data_text = driver.find_elements_by_class_name("update-item")
    update_data_dates = driver.find_elements_by_class_name("date")

    updates_text = []
    updates_dates = []

    for update in update_data_text:
        updates_text.append(update.text)

    for update in update_data_dates:
        updates_dates.append(update.text)

    return [updates_text, updates_dates]

def get_team(driver):
    team_button = driver.find_element_by_xpath("""//*[@id="tab_team"]""")
    team_button.click()

    time.sleep(0.5)         # need to sleep each time you switch the page

    member_data = driver.find_elements_by_css_selector(".card-module.team-card")

    members = []
    roles = []

    for member in member_data:
        lines = member.text.splitlines()
        members.append(lines[0]);
        roles.append(lines[1:(len(lines))])

    return [members, roles]

def get_supporters_and_dates(driver):
    community_button = driver.find_element_by_xpath("""//*[@id="tab_community"]""")
    community_button.click()
    time.sleep(0.5)

    page_nums = driver.find_element_by_class_name("pagination").text
    str_length = len(page_nums)
    tabs = ""       # algorithm only works for 1 and 2-digit numbers, so domain 1 < x < 99

    if str_length <= 9:
        tabs = str_length
    else:
        page_nums = page_nums[9:(str_length + 1)]
        str_length = len(page_nums)
        tabs = page_nums[str_length - 2:str_length]

    tabs = int(tabs);

    supporter_names = [];
    supporter_dates = [];
    supporter_times = [];

    for counter in range(1, tabs + 1):
        entries = driver.find_elements_by_class_name("supporter-item")

        for entry in entries:
            lines = entry.text.splitlines()

            if (len(lines) < 3):
                lines.insert(0, "N/A")

            supporter_names.append(lines[0])
            full_date = lines[2].split()
            date = full_date[1] + " " + full_date[2]
            clock = full_date[4] + " " + full_date[5]
            supporter_dates.append(date)
            supporter_times.append(clock)

        next_button = driver.find_element_by_class_name("pageNext")
        next_button.click();
        time.sleep(0.5)

    size_date = len(supporter_dates)
    size_time = len(supporter_times)

    if size_date > 0 and size_time > 0:
        start_date = supporter_dates[size_date - 1] + " " + supporter_times[size_time - 1]
        end_date = supporter_dates[0] + " " + supporter_times[0]
    else:
        start_date = "N/A"
        end_date = "N/A"

    return [supporter_names, supporter_dates, supporter_times, start_date, end_date]


# Extraneous methods

def convert_money(money):
    money = money[1:len(money)]
    parts = money.split(",")
    size = len(parts)

    money_string = "";                  # convert 123,456 to 123456
    for counter in range(0, size):
        money_string = money_string + parts[counter]

    money_int = int(money_string)
    return money_int
