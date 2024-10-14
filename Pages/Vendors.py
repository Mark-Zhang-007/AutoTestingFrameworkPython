from Pages.basepage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from reportportal_client import step

class VendorsPage(BasePage):
    def __init__(self, driver, logger) -> None:
        super().__init__(driver, logger)
        page_content_locator = (By.XPATH, "//div[@id='content']/h1")
        self.wait_expected_condition(EC.text_to_be_present_in_element(page_content_locator, "Select vendor to change"))        
        self.logger.info("Page: [Vendors] has been loaded successfully!")

    def is_vendor_exists(self, value) -> bool:
        self.logger.info(f"Try to check if specific Vendor <<{value}>> exists")
        single_vendor_locator = (By.XPATH, f"//table[@id='result_list']/tbody//tr/th/a[.='{value}']")
        ele_single_vendor = self.get_element(single_vendor_locator)
        if ele_single_vendor is not None and ele_single_vendor.is_displayed() and ele_single_vendor.is_enabled():
            return True
        else:
            return False
        
    # Select "Delete" action type
    def select_action_type(self, value="delete_selected"):
        self.logger.info("select action type")
        action_type_locator = (By.NAME, "action")
        self.select(action_type_locator, value)

    # Select single vendor
    def select_single_vendor(self, value:str):
        self.logger.info(f"Try to select specific Vendor <<{value}>>")
        single_vendor_chk_locator = (By.XPATH, f"//table[@id='result_list']/tbody//tr/th/a[.='{value}']//ancestor::tr/td/input[@type='checkbox']")
        self.click_chk(single_vendor_chk_locator, True)

    # Select multiple vendors
    def select_vendors(self, values:list):
        self.logger.info(f"Select vendor(s): {values}")
        for item in values:
            self.select_single_vendor(item)

    def go_click(self):
        self.logger.info("click Go button")
        submit_locator = (By.XPATH, "//div[@class='actions']//button[.='Go']")
        self.click(submit_locator)

    # Click "Add Vendor" button
    def add_vendor_click(self):
        self.logger.info("Try to add new vendor")
        add_vendor_locator = (By.XPATH, "//div[@id='content-main']//li/a")
        self.click(add_vendor_locator)
        # wait for new vendor page loading successfully
        page_content_locator = (By.XPATH, "//div[@id='content']/h1")
        self.wait_expected_condition(EC.text_to_be_present_in_element(page_content_locator, "Add vendor"))        
        self.logger.info("Page: [Add Vendor] has been loaded successfully!")

    @step("Add new vendor")
    def input_vendor_name(self, value):
        self.logger.info(f"input new vendor name: <<{value}>>")
        vendor_name_locator = (By.ID, "id_name")
        self.input(vendor_name_locator, value)

    def save_click(self):
        self.logger.info("click Save button")
        save_locator = (By.XPATH, "//div[@class='submit-row']/input[@value='Save']")
        self.click(save_locator)

    def delete_vendor(self, vendor_name):
        if self.is_vendor_exists(vendor_name):
            self.select_single_vendor(vendor_name)
            self.select_action_type()
            self.go_click()
            # wait for "Yes" button display
            yes_locator = (By.XPATH, "//div[@id='content']//form//input[@type='submit']")
            self.wait_expected_condition(EC.presence_of_element_located(yes_locator))
            self.click(yes_locator)

            delete_message_ele = self.get_message()
            self.logger.info(f"Delete Message: <<{delete_message_ele.text}>>")
        else:
            self.logger.warn(f"The vendor with name: <<{vendor_name}>> not exists, no need to delete!")

    def add_new_vendor(self, vendor_name):
        self.delete_vendor(vendor_name)
        self.add_vendor_click()
        self.input_vendor_name(vendor_name)
        self.save_click()
        add_message_ele = self.get_message()
        self.logger.info(f"Add New Vendor Message: <<{add_message_ele.text}>>")

    def get_message(self):
        message_locator = (By.XPATH, "//ul[@class='messagelist']/li[@class='success']")
        self.wait_expected_condition(EC.presence_of_element_located(message_locator))
        self.wait_expected_condition(EC.visibility_of_element_located(message_locator))

        ele_message = self.get_element(message_locator)
        return ele_message
    