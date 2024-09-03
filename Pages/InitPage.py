from Pages.Menus import MenuPage
from Pages.basepage import BasePage
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import logging
from reportportal_client import step

class InitPage(BasePage):
    def __init__(self, driver, logger) -> None:
        super().__init__(driver, logger)
        self.logger.info("Page: [Init] has been loaded successfully!")
    
    def open(self, url):
        self.logger.info(f"Init Page open: {url}")
        self.driver.get(url)

    def input_user_name(self, value:str):
        self.logger.info("input user name")
        username_locator = (By.ID, "id_username")
        self.input(username_locator, value)

    def input_password(self, value:str):
        self.logger.info("input user password")
        password_locator = (By.ID, "id_password")
        self.input(password_locator, value)

    def login(self, user_name, password):
        self.input_credential(user_name, password)
        self.logger.info("click login button")
        login_locator = (By.XPATH, "//input[@value='Log in']")
        self.click(login_locator)
        return MenuPage(self.driver, self.logger)

    @step("Input Login Credentials")
    def input_credential(self, user_name, password):
        self.logger.info("input credential data")
        self.input_user_name(user_name)
        self.input_password(password)