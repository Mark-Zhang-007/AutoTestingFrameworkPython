from Pages.basepage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from reportportal_client import step

class StudiesPage(BasePage):
    def __init__(self, driver, logger) -> None:
        super().__init__(driver, logger)
        page_content_locator = (By.XPATH, "//div[@id='content']/h1")
        self.wait_expected_condition(EC.text_to_be_present_in_element(page_content_locator, "Select study to change"))        
        self.logger.info("Page: [Studies] has been loaded successfully!")

    def is_study_exists(self, value) -> bool:
        self.logger.info(f"Try to check if specific Study <<{value}>> exists")
        single_study_locator = (By.XPATH, f"//table[@id='result_list']/tbody//tr/th/a[.='{value}']")
        ele_single_study = self.get_element(single_study_locator)
        if ele_single_study is not None and ele_single_study.is_displayed() and ele_single_study.is_enabled():
            return True
        else:
            return False
        
    # Select "Delete" action type
    def select_action_type(self, value="delete_selected"):
        self.logger.info("select action type")
        action_type_locator = (By.NAME, "action")
        self.select(action_type_locator, value)

    # Select single study
    def select_single_study(self, value:str):
        self.logger.info(f"Try to select specific Study <<{value}>>")
        single_study_chk_locator = (By.XPATH, f"//table[@id='result_list']/tbody//tr/th/a[.='{value}']//ancestor::tr/td/input[@type='checkbox']")
        self.click_chk(single_study_chk_locator, True)

    # Select multiple studies
    def select_studies(self, values:list):
        self.logger.info(f"Select studies: {values}")
        for item in values:
            self.select_single_study(item)

    def go_click(self):
        self.logger.info("click Go button")
        submit_locator = (By.XPATH, "//div[@class='actions']//button[.='Go']")
        self.click(submit_locator)

    # Click "Add Study" button
    def add_study_click(self):
        self.logger.info("Try to add new study")
        add_study_locator = (By.XPATH, "//div[@id='content-main']//li/a")
        self.click(add_study_locator)
        # wait for new study page loading successfully
        page_content_locator = (By.XPATH, "//div[@id='content']/h1")
        self.wait_expected_condition(EC.text_to_be_present_in_element(page_content_locator, "Add study"))        
        self.logger.info("Page: [Add Study] has been loaded successfully!")

    @step("Add new study - Azt id")
    def input_study_azt_id(self, value):
        self.logger.info(f"input new study Azt id: <<{value}>>")
        study_aztid_locator = (By.ID, "id_azt_id")
        self.input(study_aztid_locator, value)

    @step("Add new study - Uri")
    def input_study_uri(self, value):
        self.logger.info(f"input new study Uri: <<{value}>>")
        study_uri_locator = (By.ID, "id_uri")
        self.input(study_uri_locator, value)

    def save_click(self):
        self.logger.info("click Save button")
        save_locator = (By.XPATH, "//div[@class='submit-row']/input[@value='Save']")
        self.click(save_locator)

    def delete_study(self, study_azt_id):
        if self.is_study_exists(study_azt_id):
            self.select_single_study(study_azt_id)
            self.select_action_type()
            self.go_click()
            # wait for "Yes" button display
            yes_locator = (By.XPATH, "//div[@id='content']//form//input[@type='submit']")
            self.wait_expected_condition(EC.presence_of_element_located(yes_locator))
            self.click(yes_locator)

            delete_message_ele = self.get_message()
            self.logger.info(f"Delete Message: <<{delete_message_ele.text}>>")
        else:
            self.logger.warn(f"The study with name: <<{study_azt_id}>> not exists, no need to delete!")

    def add_new_study(self, study_azt_id, study_uri):
        self.delete_study(study_azt_id)
        self.add_study_click()
        self.input_study_azt_id(study_azt_id)
        self.input_study_uri(study_uri)
        self.save_click()
        add_message_ele = self.get_message()
        self.logger.info(f"Add New Study Message: <<{add_message_ele.text}>>")

    
    