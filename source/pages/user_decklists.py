from urls import UrlConstants
import re


class UserDecklists(UrlConstants):
    TAPPEDOUT_DECKNAME_CLASSES = "name deck-wide-header"
    TAPPEDOUT_PAGINATION = "pagination"

    def __init__(self, browser):
        self.browser = browser

    def navigate_to_users_decklists(self, username):
        self.browser.get(self.TAPPEDOUT_USER_PAGE + username + self.TAPPEDOUT_USER_DECKLIST)

    def navigate_to_users_decklist_page(self, username, page):
        self.browser.get(
            self.TAPPEDOUT_USER_PAGE +
            username +
            self.TAPPEDOUT_USER_DECKLIST +
            self.TAPPEDOUT_PAGE +
            str(page)
        )

    def get_users_decklists_names_for_user(self, username):
        self.navigate_to_users_decklist_page(username, 1)
        decknames = {}
        index = 1

        while index < self.get_number_of_pages():
            elements = self.browser.find_elements_by_class_name(
                self.TAPPEDOUT_DECKNAME_CLASSES.split(" ")[-1]
            )

            for element in elements:
                if element.get_attribute("class") == self.TAPPEDOUT_DECKNAME_CLASSES:
                    decknames[self.get_decklist_name(element)] = self.get_decklist_url(element)
            index = index + 1
            self.navigate_to_users_decklist_page(username, index)
        return decknames

    def get_decklist_name(self, name_element):
        pattern = re.compile("^mtg decks - ")
        for element in name_element.find_elements_by_tag_name("a"):
            if pattern.match(element.get_attribute("title")):
                return element.text

    def get_decklist_url(self, decklist_url_element):
        pattern = re.compile("^mtg decks - ")
        for element in decklist_url_element.find_elements_by_tag_name("a"):
            if pattern.match(element.get_attribute("title")):
                return element.get_attribute("href")

    def get_number_of_pages(self):
        pagination_element = self.browser.find_element_by_class_name(self.TAPPEDOUT_PAGINATION)
        return len(pagination_element.find_elements_by_tag_name("li"))
