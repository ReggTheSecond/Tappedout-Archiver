import re


def card_still_in_maindeck(card_name, decklist):
    return still_in_maindeck


def same_number_of_card_in_maindeck(card_name, number_of_card, decklist):
    return same_number_of_card


def same_number_of_card_in_sideboard(card_name, number_of_card, decklist):
    return same_number_of_card


def card_still_in_sideboard(card_name, decklist):
    return still_in_sideboard


def get_metadata(decklist):
    metadata = None
    for line in decklist.splitlines():
        if is_metadata(line) and metadata is None:
            metadata = "%s\n" % line
        elif is_metadata(line):
            metadata += "%s\n" % line
    return metadata


def get_maindeck(decklist):
    maindeck = None
    sideboard_started = False
    for line in decklist.splitlines():
        if re.search("Sideboard:", line):
            sideboard_started = True
        if is_in_maindeck(get_card_name(line), decklist) and maindeck is None and not sideboard_started:
            maindeck = "%s\n" % line
        elif is_in_maindeck(get_card_name(line), decklist) and not sideboard_started and line != "":
            maindeck += "%s\n" % line
    return maindeck


def get_sideboard(decklist):
    sideboard = None
    sideboard_started = False
    for line in decklist.splitlines():
        if re.search("Sideboard:", line):
            sideboard_started = True
        if is_in_sideboard(get_card_name(line), decklist) and sideboard is None and sideboard_started:
            sideboard = "%s\n" % line
        elif is_in_sideboard(get_card_name(line), decklist) and sideboard_started and line != "":
            sideboard += "%s\n" % line
    return sideboard


def is_metadata(text):
    if re.search(
        "^(Deck Name:)|(Username:)|(Date:)|(Format:)",
        text
    ):
        return True
    else:
        return False


def is_in_maindeck(card, decklist):
    maindeck_started = False
    for line in decklist.splitlines():
        if re.search("Mainboard:", line):
            maindeck_started = True
        elif re.search("Sideboard:", line):
            maindeck_started = False
        elif maindeck_started:
            if re.search(card, line):
                return True
    return False


def is_in_sideboard(card, decklist):
    sideboard_started = False
    for line in decklist.splitlines():
        if re.search("Sideboard:", line):
            sideboard_started = True
        elif sideboard_started:
            if re.search(card, line):
                return True
    return False


def get_card_name(line):
    return re.split("^\dx ", line)[-1]


def get_number_of_card(line):
    return int(re.split("x .+$", line)[0])


def compare_decklist(old_maindeck, new_maindeck):
    differences = {}
    for line in old_maindeck.splitlines():
        if(
            card_in_list(line, new_maindeck) and
            same_number_of_card_in_list(line, new_maindeck)
        ):
            pass
        elif(
            card_in_list(get_card_name(line), new_maindeck) and not
            same_number_of_card_in_list(line, new_maindeck)
        ):
            differences[get_card_name(line)] = get_difference_number_of_card(line, new_maindeck)
        elif not card_in_list(get_card_name(line), new_maindeck):
            differences[get_card_name(line)] = -get_number_of_card(line)
    return differences


def card_in_list(name_of_card, list_of_cards):
    card_in_list = False
    for card in list_of_cards.splitlines():
        if name_of_card == get_card_name(card):
            card_in_list = True
    return card_in_list


def same_number_of_card_in_list(card_details, list_of_cards):
    number_of_card_in_list = False
    for card in list_of_cards.splitlines():
        if card_in_list(get_card_name(card_details), list_of_cards):
            if get_number_of_card(card_details) == get_number_of_card(card) and card == card_details:
                number_of_card_in_list = True
    return number_of_card_in_list


def get_difference_number_of_card(line, new_maindeck):
    difference = None
    for card in new_maindeck.splitlines():
        if difference is None:
            difference = -get_number_of_card(line)
        if get_card_name(line) == get_card_name(card):
            difference = get_number_of_card(card) - get_number_of_card(line)
    return difference
