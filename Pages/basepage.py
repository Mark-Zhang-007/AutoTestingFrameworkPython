import logging
from Utility.utils import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
import traceback


class BasePage():
    def __init__(self, driver, logger:logging.Logger) -> None:
        self.driver = driver
        self.logger = logger
        # wait for page status to be ready
        self.logger.info("Current Page Status: " + self.driver.execute_script("return document.readyState;"))
        counter = 0
        while (self.driver.execute_script("return document.readyState;")!="complete" and counter<=5):
            wait(1, "Wait for page loading completed")
            counter +=1
        self.logger.info("Page loading completed now!")

    def navigate_to(self, locator):
        self.logger.info(f"Try to navigate to element: [{locator}]")
        try:            
            menu_ele = self.driver.find_element(*locator)
            if menu_ele.is_displayed() and menu_ele.is_enabled():
                menu_ele.click()
                wait(WAIT_TIME_1S, "Menu Navigating")
            else:
                self.logger.info("Menu/Link not displayed now, pls re-check!")
        except Exception as e:
            self.logger.error(f"Exception occurred with message: [{str(e)}]")
            self.logger.error(traceback.format_exc())

    def get_element(self, locator:tuple) -> WebElement:
        self.logger.info(f"Try to find element: [{locator}]")
        try:
            ele = self.driver.find_element(*locator)
            return ele
        except Exception as e:
            self.logger.error(f"Exception occurred with message: [{str(e)}]")
            self.logger.error(traceback.format_exc())
        return None
    
    def get_elements(self, locator:tuple) -> WebElement:
        self.logger.info(f"Try to find element: [{locator}]")
        try:
            eles = self.driver.find_elements(*locator)
            return eles
        except Exception as e:
            self.logger.error(f"Exception occurred with message: [{str(e)}]")
            self.logger.error(traceback.format_exc())
        return None

    def input(self, locator, value):
        self.logger.info(f"Try to input value for element: [{locator}], value: [{value}]")
        try:
            ele_input = self.driver.find_element(*locator)
            ele_input.clear()
            ele_input.send_keys(value)
        except Exception as e:
            self.logger.error(f"Exception occurred with message: [{str(e)}]")
            self.logger.error(traceback.format_exc())

    def select(self, locator, value, value_type="Value"):
        self.logger.info(f"Try to select value from element: [{locator}], value: [{value}], value type: [{value_type}]")
        try:
            ele_dropdown = self.driver.find_element(*locator)
            if ele_dropdown.is_displayed and ele_dropdown.is_enabled:
                ele_select = Select(self.driver.find_element(*locator))
                if value_type.upper() in ["I", "INDEX"]:
                    ele_select.select_by_index(value)
                elif value_type.upper() in ["V", "VALUE"]:
                    ele_select.select_by_value(value)
                else:
                    ele_select.select_by_index(0)
            else:
                self.logger.debug(f"The dropdown element: [{locator}] is not enabled or displayed now!")
        except Exception as e:
            self.logger.error(f"Exception occurred with message: [{str(e)}]")
            self.logger.error(traceback.format_exc())

    def click_chk(self, locator, value:bool):
        self.logger.info(f"Try to select checkbox on element: [{locator}], value: [{value}]")
        try:
            ele_chkbox = self.driver.find_element(*locator)            
            if ele_chkbox.is_displayed and ele_chkbox.is_enabled:
                current_selected = ele_chkbox.is_selected() 
                # current_selected = ele_chkbox.get_attribute("checked")
                # current_selected = self.driver.execute_script("return document.getElementById('xxxx').checked")
                self.logger.info(f"Current Checkbox Status: [{current_selected}], Expected Selected Status: [{value}]")
                if current_selected != value:
                    ele_chkbox.click()
                else:
                    self.logger.info("No need change checkbox status")
        except Exception as e:
            self.logger.error(f"Exception occurred with message: [{str(e)}]")
            self.logger.error(traceback.format_exc())

    def click(self, locator):
        """
        Click element by locator
        """
        self.logger.info(f"Try to click on element: [{locator}]")
        try:
            ele_button = self.driver.find_element(*locator)
            self.driver.execute_script("arguments[0].scrollIntoViewIfNeeded();", ele_button)
            self.highlight(ele_button)
            ele_button.click()
        except Exception as e:
            self.logger.error(f"Exception occurred with message: [{str(e)}]")
            self.logger.error(traceback.format_exc())

    def wait_expected_condition(self, ec, timeout=30, poll_frequency=0.5):
        driver_wait = WebDriverWait(driver=self.driver, timeout=timeout, poll_frequency=poll_frequency)
        driver_wait.until(ec)

    # Highlight element
    def highlight_locator(self, locator:tuple):
        ele_highlight = self.get_element(*locator)        
        self.driver.execute_script("arguments[0].setAttribute('style', 'background: yellow; border: 2px solid red;');", ele_highlight)

    def highlight(self, element:WebElement):
        if not element.is_displayed():
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
        self.driver.execute_script("arguments[0].setAttribute('style', 'border: 2px solid red;');", element)

    # Take screenshot
    def take_screenshot(self, file_name, sub_dir="", full_screenshot=False, upload_flg=False):
        current_dt = get_dt("D")
        target_dir = os.path.join(os.getcwd(), "Screenshots", current_dt, sub_dir)
        
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        file_name = f"{get_dt('H')}_{file_name}"
        file_path = f"{os.path.join(target_dir, file_name)}"

        if full_screenshot:
            ob = Screenshot.Screenshot()
            ob.full_screenshot(self.driver, save_path=target_dir, image_name=file_name)
        else:
            self.driver.get_screenshot_as_file(file_path)

        if upload_flg:
            upload_screenshot_with_desc(file_path)

    # Get displayed message once process done
    def get_message(self):
        message_locator = (By.XPATH, "//ul[@class='messagelist']/li[@class='success']")
        self.wait_expected_condition(EC.presence_of_element_located(message_locator))
        self.wait_expected_condition(EC.visibility_of_element_located(message_locator))

        ele_message = self.get_element(message_locator)
        return ele_message
    
    # Get Dropdown Option Values, default start from 1
    def get_select_options(self, locator:tuple, start=1):
        result = []
        ele_select_options = self.get_elements(locator)
        if ele_select_options is not None:
            for item in ele_select_options:
                result.append(item.text)
        return result[start:]
        