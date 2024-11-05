from logging import Logger
import pytest
from Utility.utils import *
from Pages.InitPage import InitPage
from Pages.Menus import MenuPage
from Pages.Vendors import VendorsPage
import sys
import json


@pytest.mark.usefixtures("setup", "rp_logger")
class TestSeqAuto():

    multivendors_test_data_set = TestCaseDataset.get_multi_data("Vendors", "case_config.json", "AddMultipleVendor")
    
    @pytest.mark.parametrize("data", multivendors_test_data_set[0], ids=multivendors_test_data_set[1])
    def test_AddVendorMultiple(self, data:dict):
        
        test_data = data
        # There's no test case need to be executed for now
        if len(test_data)==0:
            return
        
        class_name = self.__class__.__name__
        test_name = sys._getframe().f_code.co_name #request.node.name

        test_id = f"{test_data['index']}_{test_data['env']}"
        sub_dir = f"{class_name}.{test_name}[{test_id}]"

        rp_logger = self.rplogger

        rp_logger.info(f"<<<<<< [{class_name}.{test_name}] Started on [{test_data['env'].upper()}] >>>>>>")
        
        rp_logger.info("Start init browser")

        driver = self.driver

        init_page = InitPage(driver, rp_logger)
        rp_logger.info("Go to seqauto pre-prod url")
        init_page.open(test_data["url"])
        wait(WAIT_TIME_5S, "SeqAuto Initialized")
        init_page.take_screenshot("InitPage.png", sub_dir, upload_flg=True)

        if "username" in test_data.keys() and "password" in test_data.keys():
            init_page.login(test_data["username"], test_data["password"])
        
        rp_logger.info(f"current url: {driver.current_url}")
        
        menu_page = MenuPage(driver, rp_logger)
        menu_page.hide_menu()
        menu_page.view_site_menu()
        menu_page.admin_menu()
        menu_page.vendors_menu()
        vendors_page = VendorsPage(driver, rp_logger)
        vendors_page.take_screenshot("Before_AddVendor.png", sub_dir, upload_flg=True)
        vendors_page.add_new_vendor(test_data["vendorname"])
        vendors_page.take_screenshot("After_AddVendor.png", sub_dir, upload_flg=True)        
        rp_logger.info(f"<<<<<< [{class_name}.{test_name}] Ended >>>>>>")

    def test_single_vendor(self):
        test_data = TestCaseDataset.get_single_data("Vendors", "case_config.json", "AddSingleVendor")
        if test_data is None:
            return
        
        class_name = self.__class__.__name__
        test_name = sys._getframe().f_code.co_name #request.node.name

        test_id = f"{test_data['index']}_{test_data['env']}"
        sub_dir = f"{class_name}.{test_name}[{test_id}]"

        rp_logger = self.rplogger

        rp_logger.info(f"<<<<<< [{class_name}.{test_name}] Started on [{test_data['env'].upper()}] >>>>>>")
        
        rp_logger.info("Start init browser")

        driver = self.driver

        init_page = InitPage(driver, rp_logger)
        rp_logger.info("Go to seqauto pre-prod url")
        init_page.open(test_data["url"])
        wait(WAIT_TIME_5S, "SeqAuto Initialized")
        init_page.take_screenshot("InitPage.png", sub_dir, upload_flg=True)

        if "username" in test_data.keys() and "password" in test_data.keys():
            init_page.login(test_data["username"], test_data["password"])
        
        rp_logger.info(f"current url: {driver.current_url}")
        
        menu_page = MenuPage(driver, rp_logger)
        menu_page.hide_menu()
        menu_page.view_site_menu()
        menu_page.admin_menu()
        menu_page.vendors_menu()
        vendors_page = VendorsPage(driver, rp_logger)
        vendors_page.take_screenshot("BeforeAddVendor.png", sub_dir, upload_flg=True)
        vendors_page.add_new_vendor(test_data["vendorname"])
        vendors_page.take_screenshot("AfterAddVendor.png", sub_dir, upload_flg=True)
        rp_logger.info(f"<<<<<< [{class_name}.{test_name}] Ended >>>>>>")