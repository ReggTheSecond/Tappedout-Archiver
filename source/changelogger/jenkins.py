from requests_html import HTMLSession
import re


url = 'http://178.62.75.87:8080/view/TappedOut%20Archiver/job/Archive%20Tappedout/lastSuccessfulBuild/artifact/data/'
session = HTMLSession()

r = session.get(url, auth=('GreatIrishElk', 'B8asd@lkj9'))
the_usernames = [
    "ReggTheSecond"
]


def find_deck_names(username):
    response = session.get(
        '{}{}'.format(
            url,
            username
        ),
        auth=(
            'GreatIrishElk',
            'B8asd@lkj9'
        )
    )
    deck_names_link = {}
    for link in response.html.links:
        if re.search('.txt$', link):
            for line in response.text.splitlines():
                if re.search(link, line):
                    deck_name = re.sub('.+{}">|</a></td>.+'.format(link), '', line)
                    deck_names_link[deck_name] = link
    return deck_names_link


def download_deck(username, deck_name):

    response = session.get(
        '{}{}/{}'.format(
            url,
            username,
            deck_name
        ),
        auth=(
            'GreatIrishElk',
            'B8asd@lkj9'
        )
    )
    return response.text

