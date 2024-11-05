from logging import Logger
import pytest
from Utility.utils import *
from Pages.InitPage import InitPage
from Pages.Menus import MenuPage
from Pages.Studies import StudiesPage
import sys
import json


@pytest.mark.usefixtures("setup", "rp_logger")
class TestSeqAuto():

    multistudies_test_data_set = TestCaseDataset.get_multi_data("Studies", "case_config.json", "AddMultipleStudy")
    
    @pytest.mark.parametrize("data", multistudies_test_data_set[0], ids=multistudies_test_data_set[1])
    def test_AddStudyMultiple(self, data:dict):
        
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
        menu_page.studies_menu()
        studies_page = StudiesPage(driver, rp_logger)
        studies_page.take_screenshot("Before_AddStudy.png", sub_dir, upload_flg=True)
        studies_page.add_new_study(test_data["aztid"], test_data["azturi"])
        studies_page.take_screenshot("After_AddStudy.png", sub_dir, upload_flg=True)

        # Verify if new added study can be listed in External Project Page
        menu_page.view_site_menu()
        external_project_page = menu_page.external_project_menu()
        latest_studies = external_project_page.get_studies()
        rp_logger.info(f"latest studies: <<{';'.join(latest_studies)}>>")
        
        assert test_data["aztid"] in latest_studies, f"New added study: <<{test_data['aztid']}>>, latest studies: <<{';'.join(latest_studies)}>>"

        rp_logger.info(f"<<<<<< [{class_name}.{test_name}] Ended >>>>>>")

    def test_single_study(self):
        test_data = TestCaseDataset.get_single_data("Studies", "case_config.json", "AddSingleStudy")
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
        
        studies_page = menu_page.studies_menu() # StudiesPage(driver, rp_logger)        
        studies_page.take_screenshot("Before_AddStudy.png", sub_dir, upload_flg=True)
        studies_page.add_new_study(test_data["aztid"], test_data["azturi"])
        studies_page.take_screenshot("After_AddStudy.png", sub_dir, upload_flg=True)

        # Verify if new added study can be listed in External Project Page
        menu_page.view_site_menu()
        external_project_page = menu_page.external_project_menu()
        latest_studies = external_project_page.get_studies()
        rp_logger.info(f"latest studies: <<{';'.join(latest_studies)}>>")

        assert test_data["aztid"] in latest_studies, f"New added study: <<{test_data['aztid']}>>, latest studies: <<{';'.join(latest_studies)}>>"

        rp_logger.info(f"<<<<<< [{class_name}.{test_name}] Ended >>>>>>")

    