from Pages.basepage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import logging
from reportportal_client import step

class ExternalProjectPage(BasePage):
    def __init__(self, driver, logger) -> None:
        super().__init__(driver, logger)
        processing_env_locator = (By.ID, "id_processing_environment")
        self.wait_expected_condition(EC.presence_of_element_located(processing_env_locator))        
        self.logger.info("Page: [External Project] has been loaded successfully!")

    def select_processing_env(self, value=0):
        # Processing Environment
        self.logger.info("select processing environment")
        processing_env_locator = (By.ID, "id_processing_environment")
        self.select(processing_env_locator, value, "Index")

    def input_samples(self, value):
        self.logger.info("select samples")
        select_samples_locator = (By.ID, "id_samples")
        self.input(locator=select_samples_locator, value=value)

    def input_run_ids(self, value:list):
        self.logger.info("input run ids")
        run_id_1_locator = (By.ID, "id_run_id_1")
        run_id_2_locator = (By.ID, "id_run_id_2")
        run_id_3_locator = (By.ID, "id_run_id_3")
        self.input(run_id_1_locator, value[1])
        self.input(run_id_2_locator, value[2])
        self.input(run_id_3_locator, value[3])

    def select_sample_type(self, value):
        self.logger.info("select sample type")
        sample_type_locator = (By.ID, "id_sample_type")
        self.select(sample_type_locator, value)

    def select_sequencing_type(self, value):
        self.logger.info("select sequencing type")
        sequencing_type_locator = (By.ID, "id_sequencing_type")
        self.select(sequencing_type_locator, value)

    def select_analysis_type(self, value):
        self.logger.info("select analysis type")
        analysis_type_locator = (By.ID, "id_analysis_type")
        self.select(analysis_type_locator, value)

    def select_panel(self, value):
        self.logger.info("select panel")
        panel_locator = (By.ID, "id_panel")
        self.select(panel_locator, value)

    def select_reference_genome(self, value):
        self.logger.info("select reference genome")
        reference_genome_locator = (By.ID, "id_reference_genome")
        self.select(reference_genome_locator, value)

    def select_tn_dragen(self, value:bool):
        self.logger.info("Dragen Tumor/Normal Option")
        tumor_normal_locator = (By.ID, "id_tn_dragen")
        self.click_chk(tumor_normal_locator, value)

    def input_tn_dragen_config(self, value):
        self.logger.info("select Dragen Tumor/Normal Batch CSV")
        tn_dragen_config_locator = (By.ID, "id_tn_dragen_config")
        self.input(locator=tn_dragen_config_locator, value=value)


    def input_samples_per_batch(self, value:int):
        self.logger.info("input samples per batch")
        samples_per_batch_locator = (By.ID, "id_samples_per_batch")
        self.input(samples_per_batch_locator, value)

    def submit(self):
        self.logger.info("click submit button")
        submit_locator = (By.XPATH, "//input[@value='Submit']")
        self.click(submit_locator)

    @step("Submit External Project with test data")
    def submit_data(self, **kwargs):
        self.logger.info("submit all fields data")
        self.select_processing_env(kwargs["processingenv"])
        self.input_samples(kwargs["samples"])
        self.input_run_ids(kwargs["runids"])
        self.select_sample_type(kwargs["sampletype"])
        
        if "sequencingtype" in kwargs.keys() and kwargs["sequencingtype"] is not None:
            self.select_sequencing_type(kwargs["sequencingtype"])
        
        if "analysistype" in kwargs.keys() and kwargs["analysistype"] is not None:
            self.select_analysis_type(kwargs["analysistype"])

        if kwargs["panel"] is not None:
            self.select_panel(kwargs["panel"])
        else:
            self.logger.debug("No need select panel!")
        self.select_reference_genome(kwargs["referencegenome"])

        if "tumornormal" in kwargs.keys() and kwargs["tumornormal"] is not None:
            self.select_tn_dragen(kwargs["tumornormal"])

        if "batchfile" in kwargs.keys() and kwargs["batchfile"] is not None:
            self.input_tn_dragen_config(kwargs["batchfile"])

        if "samplesperbatch" in kwargs.keys() and kwargs["samplesperbatch"] is not None:
            self.input_samples_per_batch(kwargs["samplesperbatch"])

    def get_message(self):
        message_locator = (By.XPATH, "//ul[@class='messagelist']/li[@class='success']")
        self.wait_expected_condition(EC.presence_of_element_located(message_locator))
        self.wait_expected_condition(EC.visibility_of_element_located(message_locator))

        ele_message = self.get_element(message_locator)
        return ele_message
    