import unittest
from tests.changelog_tests import is_metadata
from tests.changelog_tests import is_in_maindeck
from tests.changelog_tests import is_in_sideboard
from tests.changelog_tests import get_metadata
from tests.changelog_tests import get_maindeck
from tests.changelog_tests import get_sideboard
from tests.changelog_tests import get_card_name
from tests.changelog_tests import compare_decklist
from tests.changelog_tests import card_in_list
from tests.changelog_tests import same_number_of_card_in_list
from tests.changelog_tests import get_number_of_card
from tests.changelog_tests import get_difference_number_of_card


class DeckListTests(unittest.TestCase):
    DECKLIST = """Deck Name: test
Username: ReggTheSecond
Date: 04/Jan/2019
Mainboard:
1x Abzan Kin-Guard
1x Ajani's Chosen
1x Akiri, Line-Slinger
1x Circle of Protection: Artifacts
3x Sarpadian Empires, Vol. VII
1x Prepare / Fight
1x Turn / Burn
10x Borrowing 100,000 Arrows
1x Kaboom!

Sideboard:
2x Sarpadian Empires, Vol. VII
1x Abu Ja'far
1x Adamaro, First to Desire
1x Ahn-Crop Champion
1x Appeal / Authority
1x Circle of Protection: Green
8x Research / Development
1x To Arms!"""

    NEW_DECKLIST = """Deck Name: test
Username: ReggTheSecond
Date: 04/Jan/2019
Mainboard:
2x Abzan Kin-Guard
1x Akiri, Line-Slinger
3x Circle of Protection: Artifacts
3x Sarpadian Empires, Vol. VII
1x Prepare / Fight
4x Turn / Burn
10x Borrowing 100,000 Arrows
1x Kaboom!

Sideboard:
2x Sarpadian Empires, Vol. VII
1x Abu Ja'far
1x Adamaro, First to Desire
1x Ahn-Crop Champion
1x Appeal / Authority
1x Circle of Protection: Green
8x Research / Development
1x To Arms!"""

    def test_get_metadata(self):
        expected_metadata = """Deck Name: test
Username: ReggTheSecond
Date: 04/Jan/2019
"""
        self.assertEqual(
            get_metadata(self.DECKLIST),
            expected_metadata,
            repr(
                "Expected: %s\n\nGot: %s"
                % (expected_metadata, get_metadata(self.DECKLIST))
            )
        )

    def test_is_metadata(self):
        data = {
            "Deck Name:":                         True,
            "Decklist:":                          False,
            "Username:":                          True,
            "Format:":                            True,
            "Date:":                              True,
            "Date":                               False,
            "Format":                             False,
            "Username":                           False,
            "Decklist":                           False,
            "1x Appeal / Authority":              False,
            "1x Circle of Protection: Artifacts": False,
            "Maindeck:":                          False,
            "Sideboard:":                         False
        }
        for d in data:
            self.assertEqual(
                is_metadata(d),
                data[d],
                "For: " + d +
                "\nGot: " + str(is_metadata(d)) +
                "\nExpected:" + str(data[d]))

    def test_is_in_maindeck(self):
        cards = {
            "Abzan Kin-Guard":          True,
            "Borrowing 100,000 Arrows": True,
            "Research / Development":   False,
            "Ahn-Crop Champion":        False,
            "Date: 03/Jan/2019":        False,
            "Mainboard:":               False,
            "Sideboard:":               False
        }
        for card in cards:
            self.assertEqual(
                is_in_maindeck(card, self.DECKLIST),
                cards[card],
                "For %s\nExpected: %s\nGot: %s"
                % (card, cards[card], is_in_maindeck(card, self.DECKLIST))
            )

    def test_is_in_sideboard(self):
        cards = {
            "Abzan Kin-Guard":          False,
            "Borrowing 100,000 Arrows": False,
            "Research / Development":   True,
            "Ahn-Crop Champion":        True,
            "Date: 03/Jan/2019":        False,
            "Mainboard:":               False,
            "Sideboard:":               False
        }
        for card in cards:
            self.assertEqual(
                is_in_sideboard(card, self.DECKLIST),
                cards[card],
                "For %s\nExpected: %s\nGot: %s"
                % (card, cards[card], is_in_sideboard(card, self.DECKLIST))
            )

    def test_get_card_name(self):
        cards = {
            "1x Abzan Kin-Guard": "Abzan Kin-Guard",
            "2x Borrowing 100,000 Arrows": "Borrowing 100,000 Arrows",
            "2x Research / Development": "Research / Development",
            "4x Ahn-Crop Champion": "Ahn-Crop Champion"
        }
        for card in cards:
            self.assertEqual(
                get_card_name(card),
                cards[card],
                repr(
                    "For %s\nExpected: %s\nGot %s"
                    % (card, cards[card], get_card_name(card))
                )
            )

    def test_get_number_of_card(self):
        cards = {
            "1x Abzan Kin-Guard": 1,
            "2x Borrowing 100,000 Arrows": 2,
            "2x Research / Development": 2,
            "4x Ahn-Crop Champion": 4,
            "3x Akiri, Line-Slinger": 3
        }
        for card in cards:
            self.assertEqual(
                get_number_of_card(card),
                cards[card],
                repr(
                    "For %s\nExpected: %s\nGot %s"
                    % (card, cards[card], str(get_number_of_card(card)))
                )
            )

    def test_get_maindeck(self):
        expected_maindeck = """1x Abzan Kin-Guard
1x Ajani's Chosen
1x Akiri, Line-Slinger
1x Circle of Protection: Artifacts
3x Sarpadian Empires, Vol. VII
1x Prepare / Fight
1x Turn / Burn
10x Borrowing 100,000 Arrows
1x Kaboom!
"""
        self.assertEqual(
            get_maindeck(self.DECKLIST),
            expected_maindeck,
            repr(
                "Expected:\n%s\n\nGot:\n%s"
                % (expected_maindeck, get_maindeck(self.DECKLIST))
            )
        )

    def test_get_sideboard(self):
        expected_sideboard = """2x Sarpadian Empires, Vol. VII
1x Abu Ja'far
1x Adamaro, First to Desire
1x Ahn-Crop Champion
1x Appeal / Authority
1x Circle of Protection: Green
8x Research / Development
1x To Arms!
"""
        self.assertEqual(
            get_sideboard(self.DECKLIST),
            expected_sideboard,
            repr(
                "Expected:\n%s\n\nGot:\n%s"
                % (expected_sideboard, get_sideboard(self.DECKLIST))
            )
        )

    def test_card_in_list(self):
        list = get_maindeck(self.DECKLIST)
        cards = {
            "1x Abzan Kin-Guard": True,
            "1x Ajani's Cosen": False,
            "1x Akiri, Line-Slinger": True,
            "1x Circle of Protection: Artifacts": True,
            "3x Sarpadian Empires, Vol. VII": True,
            "1x Prepare / Fight": True,
            "1x Turn / Burn": True,
            "10x Borrowing 100,000 Arrows": True,
            "1x Kaboom!": True
        }
        for card in cards:
            self.assertEqual(
                card_in_list(get_card_name(card), list),
                cards[card],
                "For %s\nExpected %s\nGot: %s" % (
                    get_card_name(card),
                    cards[card],
                    str(card_in_list(card, list))
                )
            )

    def test_same_number_of_card_in_list(self):
        old_list = get_maindeck(self.DECKLIST)
        new_list = get_maindeck(self.NEW_DECKLIST)
        cards_against_old = {
            "1x Abzan Kin-Guard": True,
            "1x Ajani's Chosen": True,
            "1x Akiri, Line-Slinger": True,
            "2x Circle of Protection: Artifacts": False
        }
        cards_against_new = {
            "1x Abzan Kin-Guard": False,
            "1x Ajani's Chosen": False,
            "1x Akiri, Line-Slinger": True,
            "2x Circle of Protection: Artifacts": False
        }
        for card in cards_against_old:
            self.assertEqual(
                same_number_of_card_in_list(card, old_list),
                cards_against_old[card],
                "List: %s\n\nFor %s\nExpected %s\nGot: %s" % (
                    old_list,
                    card,
                    cards_against_old[card],
                    str(same_number_of_card_in_list(card, old_list))
                )
            )
        for card in cards_against_new:
            self.assertEqual(
                same_number_of_card_in_list(card, new_list),
                cards_against_new[card],
                "List: %s\n\nFor %s\nExpected %s\nGot: %s" % (
                    new_list,
                    card,
                    cards_against_new[card],
                    str(same_number_of_card_in_list(card, new_list))
                )
            )

    def test_compare_decklist(self):
        old_list = get_maindeck(self.DECKLIST)
        new_list = get_maindeck(self.NEW_DECKLIST)
        differences = {
            "Abzan Kin-Guard": 1,
            "Ajani's Chosen": -1,
            "Circle of Protection: Artifacts": 2,
            "Turn / Burn": 3
        }
        self.assertEqual(
            compare_decklist(old_list, new_list),
            differences,
            "Expected:\n%s\n\nGot:\n%s" % (
                differences,
                compare_decklist(old_list, new_list)
            )
        )

    def test_get_difference_number_of_card(self):
        cards = {
            "1x Abzan Kin-Guard": 1,
            "1x Ajani's Chosen": -1,
            "1x Akiri, Line-Slinger": 0,
            "1x Circle of Protection: Artifacts": 2,
            "3x Sarpadian Empires, Vol. VII": 0,
            "1x Prepare / Fight": 0,
            "1x Turn / Burn": 3,
            "10x Borrowing 100,000 Arrows": 0,
            "1x Kaboom!": 0
        }
        new_list = get_maindeck(self.NEW_DECKLIST)
        for card in cards:
            self.assertEqual(
                get_difference_number_of_card(card, new_list),
                cards[card],
                "For %s\nExpected %s\nGot: %s" % (
                    card,
                    str(cards[card]),
                    str(get_difference_number_of_card(card, new_list))
                )
            )
