import re


def card_still_in_maindeck(card_name, decklist):
    return still_in_maindeck

def same_number_of_card_in_maindeck(card_name, number_of_card, decklist):
    return same_number_of_card

def same_number_of_card_in_sideboard(card_name, number_of_card, decklist):
    return same_number_of_card

def card_still_in_sideboard(card_name, decklist):
    return still_in_sideboard

def trim_metadata(decklist):
    for line in decklist.splitlines():
        if not is_meta_data(line):

    return decklist

def trim_maindeck(decklist):
    return maindeck

def trim_sideboard(decklist):
    return sideboard

def is_metadata(text):
    return re.search(
        "^(Deck Name:)|(Username:)|(Date:)|(Format:)",
        text
    )
