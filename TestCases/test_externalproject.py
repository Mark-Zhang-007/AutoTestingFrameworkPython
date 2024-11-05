from logging import Logger
import pytest
from Utility.utils import *
from Pages.InitPage import InitPage
from Pages.Menus import MenuPage
from Pages.ExternalProject import ExternalProjectPage
from Pages.Transfer import TransferPage
from Pages.Analyses import AnalysesPage
from Pages.Vendors import VendorsPage
import sys
import json


@pytest.mark.usefixtures("setup", "rp_logger")
class TestSeqAuto():

    test_data_set = TestCaseDataset.get_multi_data("ExternalProject", "case_config.json", "ExternalProjectMultiple")
    
    @pytest.mark.parametrize("data", test_data_set[0], ids=test_data_set[1])
    def test_ExternalProjectMultiple(self, data:dict):
        
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
        menu_page.external_project_menu()
        menu_page.take_screenshot("MenusPage.png", sub_dir, upload_flg=True)

        external_project_page = ExternalProjectPage(driver, rp_logger)
        external_project_page.take_screenshot("BeforeSubmitExternalProject.png", sub_dir, upload_flg=True)
        # submit test data
        test_data["runids"][2] = f"{test_data['runids'][2]}_{get_dt('T')}"
        test_data["runids"].insert(0, get_dt("D"))

        test_data["samples"] = os.path.join(os.getcwd(), *test_data["samples"])

        if test_data["batchfile"] is not None:
            test_data["batchfile"] = os.path.join(os.getcwd(), *test_data["batchfile"])

        external_project_page.submit_data(**test_data)
        external_project_page.take_screenshot("BeforeSubmitExternalProject.png", sub_dir, upload_flg=True)
        external_project_page.submit()

        ele_submit_message = external_project_page.get_message()
        rp_logger.info(f"External Project Submit Message: [{ele_submit_message.text}]")
        external_project_page.take_screenshot("AfterSubmitExternalProject.png", sub_dir, upload_flg=True)

        menu_page.home_menu()
        menu_page.admin_menu()

        # wait(WAIT_TIME_150S, "Wait for Transfer Finished")
        # menu_page.transfer_menu()

        # transfer_page = TransferPage(driver, rp_logger)
        # transfers_run_id = ".".join(test_data["runids"])
        # rp_logger.info(f"Target Transfer Run ID: [{transfers_run_id}]")
        # transfer_status = transfer_page.get_single_transfer_record_status(transfers_run_id)
        # transfer_page.highlight(transfer_status)
        # transfer_page.take_screenshot("TransfersSingleRecord.png", sub_dir, upload_flg=True)
        # assert "FINISHED"==transfer_status.text.upper(), f"Transfer Record Status is not finished, but: [{transfer_status.text}]"

        # menu_page.analyses_menu()
        # analyses_page = AnalysesPage(driver, rp_logger)
        # analyses_record_id = "_".join(test_data["runids"][1:])
        # analyses_status = analyses_page.get_single_analyses_record_status(analyses_record_id)
        # rp_logger.info(f"Current analyses record with run id: [{analyses_record_id}], status is: [{analyses_status.text}]")
        # analyses_page.highlight(analyses_status)
        # analyses_page.take_screenshot("AnalysesSingleRecord.png", sub_dir, upload_flg=True)
        rp_logger.info(f"<<<<<< [{class_name}.{test_name}] Ended >>>>>>")
