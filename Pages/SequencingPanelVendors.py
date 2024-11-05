from Pages.basepage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from reportportal_client import step
from Utility.utils import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from reportportal_client import step

class SequencingPanelVendorsPage(BasePage):
    def __init__(self, driver, logger) -> None:
        super().__init__(driver, logger)
        page_content_locator = (By.XPATH, "//div[@id='content']/h1")
        self.wait_expected_condition(EC.text_to_be_present_in_element(page_content_locator, "Select sequencing panel vendor to change"))        
        self.logger.info("Page: [Sequencing Panel Vendor] has been loaded successfully!")

    def is_seqpanel_vendor_exists(self, value) -> bool:
        self.logger.info(f"Try to check if specific SeqPanel Vendor: {value} exists")
        single_seqpanel_vendor_locator = (By.XPATH, f"//table[@id='result_list']/tbody//tr/th/a[.='{value}']")
        ele_single_seqpanel_vendor = self.get_element(single_seqpanel_vendor_locator)
        if ele_single_seqpanel_vendor is not None and ele_single_seqpanel_vendor.is_displayed() and ele_single_seqpanel_vendor.is_enabled():
            return True
        else:
            return False
        
    # Select "Delete" action type
    def select_action_type(self, value="delete_selected"):
        self.logger.info("select action type")
        action_type_locator = (By.NAME, "action")
        self.select(action_type_locator, value)

    # Select single seq panel vendor
    def select_single_seqpanel_vendor(self, value:str):
        self.logger.info(f"Try to select specific SeqPanel Vendor: {value}")
        single_chk_locator = (By.XPATH, f"//table[@id='result_list']/tbody//tr/th/a[.='{value}']//ancestor::tr/td/input[@type='checkbox']")
        self.click_chk(single_chk_locator, True)

    # Select multiple seqpanel vendors
    def select_seqpanel_vendors(self, values:list):
        self.logger.info(f"Select seqpanel vendors: {values}")
        for item in values:
            self.select_single_seqpanel_vendor(item)

    def go_click(self):
        self.logger.info("click Go button")
        submit_locator = (By.XPATH, "//div[@class='actions']//button[.='Go']")
        self.click(submit_locator)

    # Click "Add Sequencing Panel Vendor" button
    def add_seqpanel_vendor_click(self):
        self.logger.info("Try to add new seqpanel vendor")
        add_seqpanel_vendor_locator = (By.XPATH, "//div[@id='content-main']//li/a")
        self.click(add_seqpanel_vendor_locator)
        # wait for new seqpanel vendor page loading successfully
        page_content_locator = (By.XPATH, "//div[@id='content']/h1")
        self.wait_expected_condition(EC.text_to_be_present_in_element(page_content_locator, "Add sequencing panel vendor"))        
        self.logger.info("Page: [Add Sequencing Panel Vendor] has been loaded successfully!")

    @step("Add new SequencingPanelVendor - Comment")
    def input_comment(self, value):
        self.logger.info(f"input comment: {value}")
        comment_locator = (By.ID, "id_comment")
        self.input(comment_locator, value)

    @step("Add new SequencingPanelVendor - Name")
    def input_name(self, value):
        self.logger.info(f"input name: <<{value}>>")
        name_locator = (By.ID, "id_name")
        self.input(name_locator, value)

    @step("Add new SequencingPanelVendor - Created by")
    def select_created_by(self, value):
        self.logger.info(f"select created by: {value}")
        
        span_locator = (By.XPATH, "//div[@class='form-row field-created_by']//span[@class='selection']")
        self.click(span_locator)
        wait(WAIT_TIME_1S)

        # search with <prid>
        ele_input_search_locator = (By.XPATH, "//input[@class='select2-search__field']")
        self.input(ele_input_search_locator, value)
        wait(WAIT_TIME_2S)

        # search result
        ele_search_result_locator = (By.XPATH, f"//ul[@id='select2-id_created_by-results']/li[.='{value}']")
        ele_search_result = self.get_element(ele_search_result_locator)
        if ele_search_result is not None and ele_search_result.is_displayed:
            ele_search_result.click()
        else:
            self.logger.error(f"The prid: {value} not found from list.")
            raise Exception(f"The prid: {value} not found from list.")
        

    @step("Add new SequencingPanelVendor - Updated by")
    def select_updated_by(self, value):
        self.logger.info(f"select updated by: {value}")
        span_locator = (By.ID, "select2-id_updated_by-container")
        
        # Re-select creator
        self.click(span_locator)
        wait(WAIT_TIME_1S)

        # search with <prid>
        ele_input_search_locator = (By.XPATH, "//input[@class='select2-search__field']")
        self.input(ele_input_search_locator, value)
        wait(WAIT_TIME_2S)

        # search result
        ele_search_result_locator = (By.XPATH, f"//ul[@id='select2-id_updated_by-results']/li[.='{value}']")
        ele_search_result = self.get_element(ele_search_result_locator)
        if ele_search_result is not None and ele_search_result.is_displayed:
            ele_search_result.click()
        else:
            self.logger.error(f"The prid: {value} not found from list.")
            raise Exception(f"The prid: {value} not found from list.")

    def save_click(self):
        self.logger.info("click Save button")
        save_locator = (By.XPATH, "//div[@class='submit-row']/input[@value='Save']")
        self.click(save_locator)

    def delete_seqpanel_vendor(self, value):
        if self.is_seqpanel_vendor_exists(value):
            self.select_single_seqpanel_vendor(value)
            self.select_action_type()
            self.go_click()
            # wait for "Yes" button display
            yes_locator = (By.XPATH, "//div[@id='content']//form//input[@type='submit']")
            self.wait_expected_condition(EC.presence_of_element_located(yes_locator))
            self.click(yes_locator)

            delete_message_ele = self.get_message()
            self.logger.info(f"Delete Message: <<{delete_message_ele.text}>>")
        else:
            self.logger.warn(f"The seqpanel vendor with name: {value} not exists, no need to delete!")

    def add_new_seqpanel_vendor(self, name, comment, creator, updater):
        self.delete_seqpanel_vendor(name)
        self.add_seqpanel_vendor_click()
        self.input_name(name)
        self.input_comment(comment)
        self.select_created_by(creator)
        self.select_updated_by(updater)
        self.save_click()
        add_message_ele = self.get_message()
        self.logger.info(f"Add New Sequencing Panel Vendor Message: {add_message_ele.text}")

    
    