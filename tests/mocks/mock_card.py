class MockCard:
    def __init__(self, card_name, class_name, tag):
        self.text = card_name
        self.class_name = class_name
        self.tag = tag

    def get_attribute(self, attribute):
        if attribute == "class":
            return self.class_name

    def find_elements_by_tag_name(self, tag):
        if tag == self.tag:
            return [MockCard(self.text, self.class_name, self.tag)]
