from tests import DeckList
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tests.mocks.mock_card import MockCard
import unittest


class DeckListTests(unittest.TestCase):
    URL = "https://tappedout.net/mtg-decks/25-12-18-test/"
    BROWSER = None
    CHROME_OPTIONS = None
    MAIN_AND_SIDEBOARD = {
        "Sarpadian Empires, Vol. VII": True
    }
    MAINBOARD = {
        "Abzan Kin-Guard":                 True,
        "Ajani's Chosen":                  True,
        "Akiri, Line-Slinger":             True,
        "Borrowing 100,000 Arrows":        True,
        "Circle of Protection: Artifacts": True,
        "Kaboom!":                         True,
        "Prepare / Fight":                 True,
        "Sarpadian Empires, Vol. VII":     True,
        "Turn / Burn":                     True
    }
    SIDEBOARD = {
        "Abu Ja'far":                  True,
        "Adamaro, First to Desire":    True,
        "Ahn-Crop Champion":           True,
        "Appeal / Authority":          True,
        "Circle of Protection: Green": True,
        "Research / Development":      True,
        "Sarpadian Empires, Vol. VII": True,
        "To Arms!":                    True
    }
    PUNCTUATION = {
        "'":   "",
        ",":   "",
        "-":   "-",
        " / ": "-",
        ":":   "",
        ".":   "",
        "!":   "",
        " ":   "-"
    }
    NUM_OF_CARDS_MAINBOARD = {
        "Sarpadian Empires, Vol. VII":     "3x",
        "Circle of Protection: Artifacts": "1x",
        "Borrowing 100,000 Arrows":        "10x"
    }
    NUM_OF_CARDS_SIDEBOARD = {
        "Sarpadian Empires, Vol. VII": "2x",
        "Research / Development":      "8x",
        "To Arms!":                    "1x"
    }

    def setUp(self):
        self.CHROME_OPTIONS = Options()
        self.CHROME_OPTIONS.add_argument("--headless")
        self.BROWSER = webdriver.Chrome(chrome_options=self.CHROME_OPTIONS)
        self.BROWSER.get(self.URL)

    def test_convert_punctuation(self):
        decklist_getter = DeckList(self.BROWSER)
        for key in self.PUNCTUATION:
            self.assertEqual(
                decklist_getter.convert_punctuation(key),
                self.PUNCTUATION[key],
                "Expected: " + key + " Got: " + decklist_getter.convert_punctuation(key)
            )

    def test_get_number_of_card_in_mainboard(self):
        decklist_getter = DeckList(self.BROWSER)
        for key in self.NUM_OF_CARDS_MAINBOARD:
            self.assertEqual(
                decklist_getter.get_number_of_card_in_mainboard(key),
                self.NUM_OF_CARDS_MAINBOARD[key],
                "Expected : " + self.NUM_OF_CARDS_MAINBOARD[key] +
                " Got: " + decklist_getter.get_number_of_card_in_mainboard(key)
            )

    def test_get_number_of_card_in_sideboard(self):
        decklist_getter = DeckList(self.BROWSER)
        for key in self.NUM_OF_CARDS_SIDEBOARD:
            self.assertEqual(
                decklist_getter.get_number_of_card_in_sideboard(key),
                self.NUM_OF_CARDS_SIDEBOARD[key],
                "Expected : " + self.NUM_OF_CARDS_SIDEBOARD[key] +
                " Got: " + decklist_getter.get_number_of_card_in_sideboard(key)
            )

    def test_is_a_mainboard_card(self):
        decklist_getter = DeckList(self.BROWSER)
        for key in self.MAINBOARD:
            self.assertEqual(
                decklist_getter.is_a_mainboard_card(key),
                self.MAINBOARD[key],
                key + " not in mainboard."
            )

    def test_is_a_sideboard_card(self):
        decklist_getter = DeckList(self.BROWSER)
        for key in self.SIDEBOARD:
            self.assertEqual(
                decklist_getter.is_a_sideboard_card(key),
                self.SIDEBOARD[key],
                key + " not in sideboard."
            )

    def test_get_mainboard(self):
        cards_in_mainboard = [
            "Abzan Kin-Guard",
            "Ajani's Chosen",
            "Akiri, Line-Slinger",
            "Circle of Protection: Artifacts",
            "Sarpadian Empires, Vol. VII",
            "Prepare / Fight",
            "Turn / Burn",
            "Borrowing 100,000 Arrows",
            "Kaboom!",
        ]
        cards = []
        for card_name in cards_in_mainboard:
            card = MockCard(card_name, "card", "a")
            cards.append(card)
        formatted_mainboard = """Mainboard:
1x Abzan Kin-Guard
1x Ajani's Chosen
1x Akiri, Line-Slinger
1x Circle of Protection: Artifacts
3x Sarpadian Empires, Vol. VII
1x Prepare / Fight
1x Turn / Burn
10x Borrowing 100,000 Arrows
1x Kaboom!"""
        decklist_getter = DeckList(self.BROWSER)
        self.assertEqual(
            decklist_getter.get_mainboard(cards),
            formatted_mainboard,
            "Expected:\n" + formatted_mainboard +
            "\n\nGot:\n" + decklist_getter.get_mainboard(cards)
        )

    def test_get_sideboard(self):
        cards_in_sideboard = [
            "Abu Ja'far",
            "Adamaro, First to Desire",
            "Ahn-Crop Champion",
            "Appeal / Authority",
            "Circle of Protection: Green",
            "Research / Development",
            "Sarpadian Empires, Vol. VII",
            "To Arms!"
        ]
        cards = []
        for card_name in cards_in_sideboard:
            card = MockCard(card_name, "card", "a")
            cards.append(card)
        formatted_sideboard = """Sideboard:
1x Abu Ja'far
1x Adamaro, First to Desire
1x Ahn-Crop Champion
1x Appeal / Authority
1x Circle of Protection: Green
8x Research / Development
2x Sarpadian Empires, Vol. VII
1x To Arms!"""
        decklist_getter = DeckList(self.BROWSER)
        self.assertEqual(
            decklist_getter.get_sideboard(cards),
            formatted_sideboard,
            "Expected:\n" + formatted_sideboard +
            "\n\nGot:\n" + decklist_getter.get_sideboard(cards)
        )
        self.assertItemsEqual(
            self.convert_to_array(decklist_getter.get_sideboard(decklist_getter.get_all_card_names())),
            self.convert_to_array(formatted_sideboard),
            "Expected:\n" + formatted_sideboard +
            "\n\nGot:\n" + decklist_getter.get_sideboard(decklist_getter.get_all_card_names())
        )

    def test_is_a_sideboard_card_and_a_maindeck_card(self):
        decklist_getter = DeckList(self.BROWSER)
        for key in self.MAIN_AND_SIDEBOARD:
            self.assertEqual(
                decklist_getter.is_a_sideboard_card_and_a_maindeck_card(key),
                self.MAIN_AND_SIDEBOARD[key],
                key + " not in sideboard and mainboard."
            )

    def test_cards_not_tokens(self):
        card1 = MockCard("Adamaro, First to Desire", "card card-token", "a")
        card2 = MockCard("Prepare / Fight", "card", "a")
        cards = [card1, card2]
        expected = [card2]
        decklist_getter = DeckList(self.BROWSER)
        self.assertEqual(
            decklist_getter.cards_not_tokens(cards)[-1].text,
            expected[-1].text,
            "Expected: " + str(expected[-1].text) +
            "\nGot: " + str(decklist_getter.cards_not_tokens(cards)[-1].text)
        )

    def test_get_list_of_cards_in_deck(self):
        cards_expected = [
            "1x Abzan Kin-Guard",
            "1x Ajani's Chosen",
            "1x Akiri, Line-Slinger",
            "1x Circle of Protection: Artifacts",
            "3x Sarpadian Empires, Vol. VII",
            "1x Prepare / Fight",
            "1x Turn / Burn",
            "10x Borrowing 100,000 Arrows",
            "1x Kaboom!",
            "1x Abu Ja'far",
            "1x Adamaro, First to Desire",
            "1x Ahn-Crop Champion",
            "1x Appeal / Authority",
            "1x Circle of Protection: Green",
            "8x Research / Development",
            "2x Sarpadian Empires, Vol. VII",
            "1x To Arms!"
        ]
        decklist_getter = DeckList(self.BROWSER)
        decklist = self.convert_to_array(decklist_getter.get_list_of_cards_in_deck())

        self.assertItemsEqual(
            decklist,
            cards_expected,
            "Expected:\n" + str(cards_expected) +
            "\n\nGot:\n" + str(decklist)
        )

    def convert_to_array(self, string_of_cards):
        decklist = []
        ignore_strings = [
            "Mainboard:",
            "Sideboard:",
            ""
        ]
        for card in string_of_cards.splitlines():
            if card.strip() not in ignore_strings:
                decklist.append(str(card).strip())
        return decklist

    def diff(self, first, second):
        second = set(second)
        return [item for item in first if item not in second]

    def test_does_contain_card(self):
        decklist_getter = DeckList(self.BROWSER)
        formatted_sideboard = """Sideboard:
1x Abu Ja'far
1x Adamaro, First to Desire
1x Ahn-Crop Champion
1x Appeal / Authority
1x Circle of Protection: Green
8x Research / Development
2x Sarpadian Empires, Vol. VII
1x To Arms!"""
        cards_to_check = {
            "Abu Ja'far":         True,
            "Abzan Kin-Guard":    False,
            "Appeal / Authority": True,
            "Turn / Burn":        False
        }
        for card in cards_to_check:
            self.assertEqual(
                decklist_getter.does_contain_card(card, formatted_sideboard),
                cards_to_check[card],
                "Expected: " + str(cards_to_check[card]) +
                " Got: " + str(decklist_getter.does_contain_card(card, formatted_sideboard))
            )


if __name__ == "__main__":
    unittest.main()
