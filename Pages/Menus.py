from Pages.Analyses import AnalysesPage
from Pages.ExternalProject import ExternalProjectPage
from Pages.Transfer import TransferPage
from Pages.basepage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import logging

# Navigate to Different Menus
class MenuPage(BasePage):
    def __init__(self, driver, logger) -> None:
        super().__init__(driver, logger)
        self.logger.info("Page: [Menus] has been loaded successfully!")

    def hide_menu(self):        
        hide_menu_locator = (By.ID, "djHideToolBarButton")
        self.navigate_to(hide_menu_locator)

    def view_site_menu(self):
        view_site_link_locator = (By.XPATH, "//div//a[.='View site']")
        self.navigate_to(view_site_link_locator)

    def home_menu(self):        
        home_locator = (By.XPATH, "//div[@id='container']//a[.='Home']")
        self.wait_expected_condition(EC.presence_of_element_located(home_locator))
        self.navigate_to(home_locator)

    def admin_menu(self):
        admin_locator = (By.XPATH, "//div[@id='container']//a[.='Admin']")
        self.wait_expected_condition(EC.presence_of_element_located(admin_locator))
        self.navigate_to(admin_locator)

    def external_project_menu(self):
        external_project_locator = (By.XPATH, "//div//a[.='External Projects']")
        self.wait_expected_condition(EC.presence_of_element_located(external_project_locator))
        self.navigate_to(external_project_locator)
        return ExternalProjectPage(self.driver, self.logger)

    def transfer_menu(self):
        transfers_side_bar_locator = (By.XPATH, "//a[.='Transfers']")
        self.wait_expected_condition(EC.presence_of_element_located(transfers_side_bar_locator))
        self.navigate_to(transfers_side_bar_locator)
        return TransferPage(self.driver, self.logger)

    def analyses_menu(self):
        analyses_side_bar_locator = (By.XPATH, "//a[.='Analyses']")
        self.wait_expected_condition(EC.presence_of_element_located(analyses_side_bar_locator))
        self.navigate_to(analyses_side_bar_locator)
        return AnalysesPage(self.driver, self.logger)
