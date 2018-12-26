from urls import UrlConstants
import re


class DeckList(UrlConstants):
    TAPPEDOUT_DECKLIST_CARD_CLASS = "card"
    TAPPEDOUT_BOARD = "board-container"

    def __init__(self, browser):
        self.browser = browser

    def navigate_to_users_decklist(self, deckname):
        self.browser.get(self.TAPPEDOUT_HOME + self.TAPPEDOUT_USER_DECKLIST + deckname)

    def get_all_card_names(self):
        boards = self.browser.find_element_by_class_name(self.TAPPEDOUT_BOARD)
        cards = boards.find_elements_by_class_name(self.TAPPEDOUT_DECKLIST_CARD_CLASS)
        return cards

    def get_list_of_cards_in_deck(self):
        decklist = ""
        cards = self.get_all_card_names()
        decklist = self.get_mainboard(cards) + "\n\n" + self.get_sideboard(cards)
        return decklist

    def get_number_of_card_in_mainboard(self, name_of_card):
        try:
            element = self.browser.find_element_by_id(
                "boardContainer-main-" + self.convert_punctuation(name_of_card)
            )
        except Exception:
            pass
        return element.find_element_by_tag_name("a").text

    def get_number_of_card_in_sideboard(self, name_of_card):
        try:
            element = self.browser.find_element_by_id(
                "boardContainer-side-" + self.convert_punctuation(name_of_card)
            )
        except Exception:
            pass
        return element.find_element_by_tag_name("a").text

    def format_decklist(self, decklist):
        mainboard = "Mainboard:\n"
        sideboard = "Sideboard:\n"
        for card in decklist.split('\n'):
            if self.is_a_mainboard_card(re.sub("(\d\d|\d)x ", "", card.strip().lower())):
                mainboard = mainboard + card + "\n"
            elif self.is_a_sideboard_card(re.sub("(\d\d|\d)x ", "", card.strip().lower())):
                sideboard = sideboard + card + "\n"
        return mainboard + sideboard

    def is_a_sideboard_card_and_a_maindeck_card(self, name_of_card):
        try:
            self.browser.find_element_by_id(
                "boardContainer-main-" + self.convert_punctuation(name_of_card)
            )
            self.browser.find_element_by_id(
                "boardContainer-side-" + self.convert_punctuation(name_of_card)
            )
            return True
        except Exception:
            return False

    def is_a_mainboard_card(self, name_of_card):
        try:
            self.browser.find_element_by_id(
                "boardContainer-main-" + self.convert_punctuation(name_of_card)
            )
            return True
        except Exception:
            return False

    def is_a_sideboard_card(self, name_of_card):
        try:
            self.browser.find_element_by_id(
                "boardContainer-side-" + self.convert_punctuation(name_of_card)
            )
            return True
        except Exception:
            return False

    def convert_punctuation(self, card_name):
        card_name = re.sub("[',:.!]", "", card_name)
        card_name = re.sub(" \/ ", "-", card_name)
        return re.sub("\s", "-", card_name).lower()

    def cards_not_tokens(self, list_of_cards):
        return_cards = []
        for card in list_of_cards:
            if card.get_attribute("class") != "card card-token" and card.text.strip() != "Flip":
                return_cards.append(card)
        return return_cards

    def get_mainboard(self, cards):
        mainboard = "Mainboard:\n"
        for card in self.cards_not_tokens(cards):
            name_of_card = card.text
            if(
                self.is_a_mainboard_card(name_of_card) and not
                self.does_contain_card(name_of_card, mainboard)
            ):
                mainboard += (
                    self.get_number_of_card_in_mainboard(name_of_card) +
                    " " + name_of_card + "\n"
                )
        return mainboard.strip()

    def get_sideboard(self, cards):
        sideboard = "Sideboard:\n"
        for card in self.cards_not_tokens(cards):
            name_of_card = card.text
            if(
                self.is_a_sideboard_card(name_of_card) and not
                self.does_contain_card(name_of_card, sideboard)
            ):
                sideboard += (
                    self.get_number_of_card_in_sideboard(name_of_card) +
                    " " + name_of_card + "\n"
                )
        return sideboard.strip()

    def does_contain_card(self, name_of_card, string_of_cards):
        return name_of_card in string_of_cards
