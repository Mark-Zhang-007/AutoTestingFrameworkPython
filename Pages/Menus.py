from Pages.Analyses import AnalysesPage
from Pages.ExternalProject import ExternalProjectPage
from Pages.Transfer import TransferPage
from Pages.Vendors import VendorsPage
from Pages.Studies import StudiesPage
from Pages.SequencingPanelVendors import SequencingPanelVendorsPage
from Pages.basepage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import logging

class MenuLocators:
    hide_menu_locator = (By.ID, "djHideToolBarButton")
    view_site_link_locator = (By.XPATH, "//div//a[.='View site']")
    home_locator = (By.XPATH, "//div[@id='container']//a[.='Home']")
    admin_locator = (By.XPATH, "//div[@id='container']//a[.='Admin']")
    external_project_locator = (By.XPATH, "//div//a[.='External Projects']")
    transfers_side_bar_locator = (By.XPATH, "//a[.='Transfers']")
    analyses_side_bar_locator = (By.XPATH, "//a[.='Analyses']")
    aggregations_side_bar_locator = (By.XPATH, "//a[.='Aggregations']")
    vendors_side_bar_locator = (By.XPATH, "//a[.='Vendors']")
    studies_side_bar_locator = (By.XPATH, "//a[.='Studies']")
    seq_panel_vendors_side_bar_locator = (By.XPATH, "//a[.='Sequencing panel vendors']")

# Navigate to Different Menus
class MenuPage(BasePage):
    def __init__(self, driver, logger) -> None:
        super().__init__(driver, logger)
        self.logger.info("Page: [Menus] has been loaded successfully!")

    def hide_menu(self):
        self.navigate_to(MenuLocators.hide_menu_locator)

    def view_site_menu(self):
        self.navigate_to(MenuLocators.view_site_link_locator)

    def home_menu(self):
        self.wait_expected_condition(EC.presence_of_element_located(MenuLocators.home_locator))
        self.navigate_to(MenuLocators.home_locator)

    def admin_menu(self):
        self.wait_expected_condition(EC.presence_of_element_located(MenuLocators.admin_locator))
        self.navigate_to(MenuLocators.admin_locator)

    def external_project_menu(self):
        self.wait_expected_condition(EC.presence_of_element_located(MenuLocators.external_project_locator))
        self.navigate_to(MenuLocators.external_project_locator)
        return ExternalProjectPage(self.driver, self.logger)

    def transfer_menu(self):
        self.wait_expected_condition(EC.presence_of_element_located(MenuLocators.transfers_side_bar_locator))
        self.navigate_to(MenuLocators.transfers_side_bar_locator)
        return TransferPage(self.driver, self.logger)

    def analyses_menu(self):
        self.wait_expected_condition(EC.presence_of_element_located(MenuLocators.analyses_side_bar_locator))
        self.navigate_to(MenuLocators.analyses_side_bar_locator)
        return AnalysesPage(self.driver, self.logger)
    
    def aggregations_menu(self):
        self.wait_expected_condition(EC.presence_of_element_located(MenuLocators.aggregations_side_bar_locator))
        self.navigate_to(MenuLocators.aggregations_side_bar_locator)
        return AnalysesPage(self.driver, self.logger)
    
    def vendors_menu(self):
        self.wait_expected_condition(EC.presence_of_element_located(MenuLocators.vendors_side_bar_locator))
        self.navigate_to(MenuLocators.vendors_side_bar_locator)
        return VendorsPage(self.driver, self.logger)
    
    def studies_menu(self):
        self.wait_expected_condition(EC.presence_of_element_located(MenuLocators.studies_side_bar_locator))
        self.navigate_to(MenuLocators.studies_side_bar_locator)
        return StudiesPage(self.driver, self.logger)
    
    def sequencing_panel_vendors_menu(self):
        self.wait_expected_condition(EC.presence_of_element_located(MenuLocators.seq_panel_vendors_side_bar_locator))
        self.navigate_to(MenuLocators.seq_panel_vendors_side_bar_locator)
        return SequencingPanelVendorsPage(self.driver, self.logger)
