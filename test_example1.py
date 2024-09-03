import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utility.utils import *


@pytest.mark.usefixtures("setup")
class TestExample:

    def test_title(self):
        self.driver.get("https://demo.seleniumeasy.com/")
        wait(15)
        assert "Selenium Easy" in self.driver.title

    def test_content_text(self):
        print("Verify content on the page")
        centerText = self.driver.find_element(by=By.CSS_SELECTOR, value=".tab-content .text-center").text
        print(centerText)
        assert "WELCOME TO SELENIUM EASY DEMO" == centerText

    def test_bootstrap_bar(self):
        print("Lets try with another example")
        mainMenu = self.driver.find_element(by=By.XPATH, value="//li/a[contains(text(), 'Progress Bars')]")
        mainMenu.click()

        subMenu = self.driver.find_element(by=By.XPATH, value="//li/a[contains(text(), 'Bootstrap Progress bar')]")
        subMenu.click()

        btnDownload = self.driver.find_element(by=By.ID, value="cricle-btn")
        btnDownload.click()

        WebDriverWait(self.driver, 50).until(EC.text_to_be_present_in_element_value((By.ID, 'cricleinput'), '105'))

        elemValue = self.driver.find_element(by=By.ID, value="cricleinput")
        elemAttributeValue = elemValue.get_attribute("value")
        assert elemAttributeValue == "105"

    def test_one(self):
        x = "this"
        assert 'h' in x

    def test_two(self):
        x = "hello"
        assert hasattr(x, 'check')

    def test_three(self):
        x = "welcome"
        assert hasattr(x, 'test')
