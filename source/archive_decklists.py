from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from source.changelogger.jenkins import find_deck_names
from source.changelogger.jenkins import download_deck
import source.pages as pages
import os
import re


def get_cwp():
    cwd = os.getcwd()
    return os.path.abspath(cwd)


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
browser = webdriver.Chrome(chrome_options=chrome_options)
page = pages.Home(browser)
page.navigate_to_home()
page.accept_cookies()

path_to_data = "/data/"
path_to_tmp = "{}/tmp".format(os.getcwd())

usernames = [
    "ReggTheSecond"
]

for username in usernames:
    if not os.path.isdir(path_to_tmp):
        os.mkdir(path_to_tmp)
    if not os.path.isdir("{}/{}".format(path_to_tmp, username)):
        os.mkdir("{}/{}".format(path_to_tmp, username))
    deck_names_links = find_deck_names(username)
    for key in deck_names_links:
        deck_list = download_deck(username, deck_names_links[key])
        file = open("{}/{}/{}".format(path_to_tmp, username, key), 'w')
        file.write(deck_list)

for username in usernames:
    page = pages.UserDecklists(browser)
    decknames_and_deck_urls = page.get_users_decklists_names_for_user(username)
    page = pages.DeckList(browser)
    dir = "{}{}{}/".format(
        get_cwp(),
        path_to_data,
        username
    )
    if not os.path.isdir(path_to_data):
        os.mkdir(get_cwp() + path_to_data)
    if not os.path.isdir(dir):
        os.mkdir(dir)

    for key in decknames_and_deck_urls:
        print(key)
        file = open(dir + re.sub("/", "-", key) + ".txt", 'w')
        date = datetime.now()
        deck_info = "Deck Name: {}\nUsername: {}\nDate: {}\n".format(
            key,
            username,
            date.strftime("%d/%b/%Y")
        )
        browser.get(decknames_and_deck_urls[key])
        decklist = page.get_list_of_cards_in_deck()
        file.write(deck_info + decklist)
        file.close()

browser.quit()
