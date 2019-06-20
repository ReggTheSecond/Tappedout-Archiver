import re


def format_changelog(diff):
    added = ""
    cut = ""
    for card in diff:
        if diff[card] > 0:
            added += "\t{}: +{}\n".format(card, diff[card])
        else:
            cut += "\t{}: {}\n".format(card, diff[card])
    return "{}{}".format(added, cut)


def has_sideboard(deck):
    return deck.strip() != ''


def format_changelog_main_and_side(old_deck, new_deck):
    changelog = "CHANGELOG:\nMaindeck\n"
    maindeck_diff = compare_decklist(
        get_maindeck(
            old_deck
        ),
        get_maindeck(
            new_deck
        )
    )
    changelog += format_changelog(maindeck_diff)
    if has_sideboard(get_sideboard(new_deck)):
        sideboard_diff = compare_decklist(
            get_sideboard(
                old_deck
            ),
            get_sideboard(
                new_deck
            )
        )
        changelog += "\nSideboard\n{}".format(
            format_changelog(sideboard_diff)
        )
    return changelog


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
    return sideboard if sideboard != None else ""


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
        elif re.search("CHANGELOG:", line):
            sideboard_started = False
        elif sideboard_started:
            if re.search(card, line):
                return True
    return False


def get_card_name(line):
    return re.split("^\dx ", line)[-1]


def get_number_of_card(line):
    return int(re.split("x .+$", line)[0]) if line != '' else 0


def compare_decklist(old_deck, new_deck):
    differences = {}
    for card in old_deck.splitlines():
        # Is card still in deck?
        if card_in_list(get_card_name(card), new_deck):
            # Has the number of the card in the deck changed?
            if not same_number_of_card_in_list(card, new_deck):
                differences[get_card_name(card)] = get_difference_number_of_card(card, new_deck)
        else:
            differences[get_card_name(card)] = -get_number_of_card(card)
    for card in new_deck.splitlines():
        # Was card in deck?
        if card_in_list(get_card_name(card), old_deck):
            # Was the same number of the card in the old deck?
            if not same_number_of_card_in_list(card, new_deck):
                differences[get_card_name(card)] = get_difference_number_of_card(card, new_deck)
        # Is card completely new?
        else:
            differences[get_card_name(card)] = get_number_of_card(card)
    return differences


def card_in_list(name_of_card, list_of_cards):
    for card in list_of_cards.splitlines():
        if re.search(name_of_card, card):
            return True
    return False


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
