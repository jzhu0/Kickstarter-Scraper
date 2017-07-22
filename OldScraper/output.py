# Printing methods

def print_elements(name, genre, type, location, amounts, num_supporters, num_followers,
                   rewards, wishlist, updates, team, community, story):
    print(name)
    print(genre)
    print(type)
    print(location)
    print(amounts)
    print(num_supporters)
    print(num_followers)
    print(rewards)
    print(wishlist)
    print(updates)
    print(team)
    print(community)

# Sorting methods

def get_file_name(name):
    file_name = name.lower()
    file_name = file_name.replace(" ", "_")
    file_name = file_name.replace(",", "")
    file_name = file_name.replace("/", "-")      # fix file path error
    file_name = file_name.replace(":", "")
    return file_name

def get_file_path(name):
    file_name = get_file_name(name)
    file_name = "csv_files/" + file_name + ".csv"
    return file_name

def polish_elements(name, genre, type, location, amounts, num_supporters, num_followers,
                   rewards, wishlist, updates, team, community, story):
    name = ['name', name]
    genre.insert(0, 'genre')
    type = ['type', type]
    location = ['location', location]
    story = ['story', story]

    amount_raised = ['amount_raised', amounts[0]]
    amount_target = ['amount_target', amounts[1]]

    num_supporters = ['num_supporters', num_supporters]
    num_followers = ['num_followers', num_followers]

    reward_amounts = rewards[0]
    reward_amounts.insert(0, 'reward_amounts')
    reward_categories = rewards[1]
    reward_categories.insert(0, 'reward_categories')

    wishlist_items = wishlist[0]
    wishlist_items.insert(0, "wishlist_items")
    wishlist_progress = wishlist[1]
    wishlist_progress.insert(0, "wishlist_progress")

    update_text = updates[0]
    update_text.insert(0, "update_text")
    update_dates = updates[1]
    update_dates.insert(0, "update_dates")

    team_members = team[0]
    team_members.insert(0, "team_members")
    team_roles = team[1]
    team_roles.insert(0, "team_roles")

    supporter_names = community[0]
    supporter_names.insert(0, "supporter_names")
    supporter_dates = community[1]
    supporter_dates.insert(0, "supporter_dates")
    supporter_times = community[2]
    supporter_times.insert(0, "supporter_times")
    start_date = ["start_date", community[3]]
    end_date = ["end_date", community[4]]

    return [name, genre, type, location, amount_raised, amount_target, start_date, end_date,
            num_supporters, num_followers, team_members, team_roles, reward_categories, reward_amounts,
            wishlist_items, wishlist_progress, supporter_names, supporter_dates, supporter_times,
            update_dates, update_text, story]
