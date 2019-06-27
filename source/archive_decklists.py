from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from source.changelogger.jenkins import find_deck_names
from source.changelogger.jenkins import download_deck
from source.changelogger.compare_versions import format_changelog_main_and_side
import source.pages as pages
import os
import re
import glob


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
browser = webdriver.Chrome(chrome_options=chrome_options)
page = pages.Home(browser)
page.navigate_to_home()
page.accept_cookies()

path_to_data = "{}/data/".format(os.getcwd())
path_to_tmp = "{}/tmp".format(os.getcwd())
print(path_to_data)
print(path_to_tmp)

globber_data = '{}**/*.txt'.format(path_to_data)
globber_tmp = '{}/**/*.txt'.format(path_to_tmp)

usernames = [
    "ReggTheSecond",
    "Karab",
    "giantlemon99"
]

for username in usernames:
    if not os.path.isdir(path_to_tmp):
        os.mkdir(path_to_tmp)
    if not os.path.isdir("{}/{}".format(path_to_tmp, username)):
        os.mkdir("{}/{}".format(path_to_tmp, username))
    deck_names_links = find_deck_names(username)
    for key in deck_names_links:
        deck_list = download_deck(username, deck_names_links[key])
        file = open(
            "{}/{}/{}".format(
                path_to_tmp,
                username,
                re.sub(
                    '\?',
                    '',
                    re.sub('/|:', '-', key)
                )
            ),
            'w'
        )
        file.write(deck_list)

for username in usernames:
    page = pages.UserDecklists(browser)
    decknames_and_deck_urls = page.get_users_decklists_names_for_user(username)
    page = pages.DeckList(browser)

    if not os.path.isdir(path_to_data):
        os.mkdir(path_to_data)
    if not os.path.isdir('{}/{}'.format(path_to_data, username)):
        os.mkdir('{}/{}'.format(path_to_data, username))

    for key in decknames_and_deck_urls:
        file = open(
            "{}/{}/{}.txt".format(
                path_to_data,
                username,
                re.sub(
                    '\?',
                    '',
                    re.sub('/|:', '-', key)
                )
            ),
            'w'
        )
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

files_from_data = glob.glob(globber_data)
files_from_tmp = glob.glob(globber_tmp)


for file_data in files_from_data:
    print(file_data)
    deck_name = file_data.split('\\')[-1]

    for file_tmp in files_from_tmp:
        if deck_name in file_tmp:
            print(file_tmp)
            new_deck = open(file_data, 'r').read()
            old_deck = open(file_tmp, 'r').read()
            
            changelog = format_changelog_main_and_side(old_deck, new_deck)
            new_deck = open(file_data, 'r').read()
            sideboard_started = False
            changelog_started = False
            deck_list = ""
            for line in new_deck.splitlines():
                if re.search('Sideboard:', line):
                    sideboard_started = True
                if re.search('CHANGELOG:', line):
                    changelog_started = True
                if not changelog_started and sideboard_started and line.strip() == "":
                    pass
                elif not changelog_started:
                    deck_list += "\n{}".format(line)

            append_deck = open(file_data, 'w')
            append_deck.write(
                deck_list
            )
            append_deck.write(
                "\n\n{}".format(changelog)
            )
            append_deck.close()
