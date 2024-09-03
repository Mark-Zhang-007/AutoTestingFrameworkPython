from Pages.basepage import BasePage
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import logging

class AnalysesPage(BasePage):
    def __init__(self, driver, logger) -> None:
        super().__init__(driver, logger)
        analyses_result_locator = (By.XPATH, "//table[@id='result_list']")
        self.wait_expected_condition(EC.presence_of_element_located(analyses_result_locator))
        self.logger.info("Page: [Analyses] has been loaded successfully!")

    def get_analyses_records(self):
        analyses_result_locator = (By.XPATH, "//table[@id='result_list']")
        self.wait_expected_condition(EC.presence_of_element_located(analyses_result_locator))
        return self.get_element(analyses_result_locator)
    
    def get_single_analyses_record_status(self, analyses_record_id) -> WebElement:
        analyses_status_locator = (By.XPATH, f"//table[@id='result_list']//td/a[contains(., '{analyses_record_id}')]//ancestor::tr/td[@class='field-state_color']/div")
        analyses_status = self.get_element(analyses_status_locator)
        self.logger.info(f"Current analyses record with run id: [{analyses_record_id}], status is: [{analyses_status.text}]")
        return analyses_status
