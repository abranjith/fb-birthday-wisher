__author__ = 'Ranjith'
'''
This script is based on base page object design pattern common in selenium framework creation.
Each page is viewed as a class and hosts all elements and functionalities that a particular page provides.
This can be imported and used by tests
'''
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class  BasePage(object):
    def __init__(self, driver):
        self.driver = driver

    def convert_this_type(self, locator_type):
        if locator_type.upper() == "ID":
            return By.ID
        elif locator_type.upper() == "NAME":
            return By.NAME
        elif locator_type.upper() == "XPATH":
            return By.XPATH
        elif locator_type.upper() == "LINK_TEXT":
            return By.LINK_TEXT
        elif locator_type.upper() == "PARTIAL_LINK_TEXT":
            return By.PARTIAL_LINK_TEXT
        elif locator_type.upper() == "TAG_NAME":
            return By.TAG_NAME

    def is_element_present(self, locator_value, locator_type="ID"):

        loc_type = self.convert_this_type(locator_type)

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((loc_type, locator_value))
            )
            return True

        except TimeoutException as e:
            return False

    def find_element_withpatience(self, locator_value, locator_type="ID", waittime=10):

        loc_type = self.convert_this_type(locator_type)

        try:
            element = WebDriverWait(self.driver, waittime).until(
                EC.presence_of_element_located((loc_type, locator_value))
            )
            return element

        except TimeoutException as e:
            raise NoSuchElementException

class  LoginPage(BasePage):

    def __init__(self, driver):
        BasePage.__init__(self, driver)
        assert self.is_element_present("email"), "Couldn't locate login page"

        self.username_input = self.find_element_withpatience("email")
        self.password_input = self.find_element_withpatience("pass")
        self.login_button = self.find_element_withpatience("loginbutton")

    def login_as(self, username, password):
        self.username_input.clear()
        self.username_input.send_keys(username)

        self.password_input.clear()
        self.password_input.send_keys(password)

        self.login_button.click()

    def login_is_successful(self, name):
        assert self.is_element_present("//*[@id='pagelet_welcome_box']/ul/li/div/div/a","XPATH"), "Not in home page"

        return name in self.find_element_withpatience("//*[@id='pagelet_welcome_box']/ul/li/div/div/a","XPATH").text

class  MainPage(BasePage):

    def goto_birthday_page(self):

        event_link = self.find_element_withpatience("//*[@id='navItem_2344061033']/a", "XPATH")
        event_link.click()

        all_bdays_link = self.find_element_withpatience("//*[@id='pagelet_birthday_this_week']/div/div[1]/div/a", "XPATH")
        all_bdays_link.click()

    def wish_them_all(self, message):
        all_bday_area = self.find_element_withpatience("//*[@id='events_birthday_view']", "XPATH")

        all_textarea_towish = all_bday_area.find_elements(By.NAME, "message")

        for textarea in all_textarea_towish:
            textarea.clear()
            textarea.send_keys(message)
            time.sleep(1)
            textarea.send_keys(Keys.ENTER)
            time.sleep(5)

if __name__ == "__main__":
    pass