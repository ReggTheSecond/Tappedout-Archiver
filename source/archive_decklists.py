from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import pages
import os


def get_cwp():
    cwd = os.getcwd()
    return os.path.abspath(cwd)


chrome_options = Options()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)
page = pages.Home(browser)
page.navigate_to_home()
page.accept_cookies()

username = "ReggTheSecond"

page = pages.UserDecklists(browser)
decknames_and_deck_urls = page.get_users_decklists_names_for_user(username)
page = pages.DeckList(browser)

try:
    os.mkdir(get_cwp() + "/data/")
except Exception:
    pass


for key in decknames_and_deck_urls:
    print key
    file = open(get_cwp() + "/data/" + key + ".txt", 'w')
    date = datetime.now()
    deck_info = "Deck Name: " + key +\
        "\nUsername: " + username +\
        "\nDate: " + date.strftime("%d/%b/%Y") +\
        "\n"
    browser.get(decknames_and_deck_urls[key])
    decklist = page.get_list_of_cards_in_deck()
    file.write(deck_info + decklist)
    file.close()

browser.quit()
