from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from source.pages.urls import UrlConstants


class Home(UrlConstants):
    TERMS_OF_SERVICE_BUTTON = "CybotCookiebotDialogBodyLevelButtonAccept"

    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(self.browser, 10)

    def navigate_to_home(self):
        self.browser.get(self.TAPPEDOUT_HOME)

    def accept_cookies(self):
        element = self.wait.until(
            EC.visibility_of_element_located(
                (By.ID, self.TERMS_OF_SERVICE_BUTTON)
            )
        )
        element.click()
