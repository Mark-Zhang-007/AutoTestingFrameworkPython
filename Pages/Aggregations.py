from Pages.basepage import BasePage
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import logging

class AggregationsPage(BasePage):
    def __init__(self, driver, logger) -> None:
        super().__init__(driver, logger)
        aggregations_result_locator = (By.XPATH, "//table[@id='result_list']")
        self.wait_expected_condition(EC.presence_of_element_located(aggregations_result_locator))
        self.logger.info("Page: [Aggregations] has been loaded successfully!")

    def get_aggregations_records(self):
        aggregations_result_locator = (By.XPATH, "//table[@id='result_list']")
        self.wait_expected_condition(EC.presence_of_element_located(aggregations_result_locator))
        return self.get_element(aggregations_result_locator)
    
    def get_single_aggregations_record_status(self, analyses_record_id) -> WebElement:
        aggregations_status_locator = (By.XPATH, f"//table[@id='result_list']//td/a[contains(., '{analyses_record_id}')]//ancestor::tr/td[@class='field-state_color']/div")
        aggregations_status = self.get_element(aggregations_status_locator)
        self.logger.info(f"Current analyses record with run id: [{analyses_record_id}], status is: [{aggregations_status.text}]")
        return aggregations_status
    
    def get_single_aggregations_record_details(self, analyses_record_id):
        aggregations_show_button_locator = (By.XPATH, f"//table[@id='result_list']//td/a[contains(., '{analyses_record_id}')]//ancestor::tr/td[@class='field-show_task']/a")
        aggregations_show_button = self.get_element(aggregations_show_button_locator)
        aggregations_show_button.click()
