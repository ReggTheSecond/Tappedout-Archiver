import unittest


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

    def test_card_still_in_maindeck():
        cards = {
            "Abzan Kin-Guard":     True,
            "Akiri, Line-Slinger": True,
            "Abu Ja'far":          False,
            "To Arms!":            False
        }
        for card in cards:
            self.assertEqual(card_still_in_maindeck(card, self.DECKLIST))

    def test_card_still_in_sideboard():
        cards = {
            "Abzan Kin-Guard":     False,
            "Akiri, Line-Slinger": False,
            "Abu Ja'far":          True,
            "To Arms!":            True
        }
        for card in cards:
            self.assertEqual(card_still_in_sideboard(card, self.DECKLIST), cards[card])

    def test_trim_metadata():
        deck_without_metadata = """Mainboard:
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
        self.assertEqual(trim_metadata(self.DECKLIST), deck_without_metadata)

    def test_trim_maindeck():
        sideboard = """2x Sarpadian Empires, Vol. VII
1x Abu Ja'far
1x Adamaro, First to Desire
1x Ahn-Crop Champion
1x Appeal / Authority
1x Circle of Protection: Green
8x Research / Development
1x To Arms!"""
        self.assertEqual(trim_maindeck(self.DECKLIST), sideboard)

    def test_trim_sideboard():
        maindeck = """1x Abzan Kin-Guard
1x Ajani's Chosen
1x Akiri, Line-Slinger
1x Circle of Protection: Artifacts
3x Sarpadian Empires, Vol. VII
1x Prepare / Fight
1x Turn / Burn
10x Borrowing 100,000 Arrows
1x Kaboom!"""
        self.assertEqual(trim_sideboard(self.DECKLIST), maindeck)

    def test_same_number_of_card_in_maindeck():
        pass

    def test_same_number_of_card_in_sideboard():
        pass

    def test_is_metadata():
        data = {
            "Decklist:":                          True,
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
            self.assertEqual(self.is_metadata, data[d])
