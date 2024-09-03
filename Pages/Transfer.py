from Pages.basepage import BasePage
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import logging

class TransferPage(BasePage):
    def __init__(self, driver, logger) -> None:
        super().__init__(driver, logger)
        transfers_result_locator = (By.XPATH, "//table[@id='result_list']")
        self.wait_expected_condition(EC.presence_of_element_located(transfers_result_locator))
        self.logger.info("Page: [Transfer] has been loaded successfully!")        
    
    def get_transfer_records(self):
        transfers_result_locator = (By.XPATH, "//table[@id='result_list']")
        self.wait_expected_condition(EC.presence_of_element_located(transfers_result_locator))
        return self.get_element(transfers_result_locator)
    
    def get_single_transfer_record_status(self, transfers_run_id) -> WebElement:
        single_transfer_record_status_locator=(By.XPATH, f"//table[@id='result_list']//td[.='{transfers_run_id}']//ancestor::tr/td[@class='field-state_color']/div")
        transfer_status = self.get_element(single_transfer_record_status_locator)
        self.logger.info(f"Transfer record with run id: [{transfers_run_id}], status is: [{transfer_status.text}]")
        return transfer_status

