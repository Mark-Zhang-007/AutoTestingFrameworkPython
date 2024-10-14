import pytest
import logging
import os
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from Utility.utils import *
import time
from reportportal_client import RPLogger, RPLogHandler
import shutil
import traceback

root_dir = os.getcwd()

@pytest.fixture()
def init_browser(request):
    global driver
    global port_index

    port_no = 9222
    
    logging.info("clean existed screenshots")    
        
    browser = "chrome"
    generate_start_chrome(port_no)

    thread_lock = threading.Lock()
    thread_chrome_launcher = threading.Thread(target=start_browser, args=[thread_lock, browser, port_no], name="StartChromeBrowser")
    thread_chrome_launcher.start()

    chrome_options = ChromeOptions()
    chrome_options.add_experimental_option('debuggerAddress', f'127.0.0.1:{port_no}')
    
    driver = webdriver.Chrome(service=ChromeService(executable_path="chromedriver.exe"), options=chrome_options)
    wait(WAIT_TIME_10S)

    driver.set_page_load_timeout(WAIT_TIME_60S)
    driver.set_script_timeout(WAIT_TIME_30S)
    driver.implicitly_wait(WAIT_TIME_5S)
    request.cls.driver = driver

    # close redundant tabs when initialize browser, just leave one active tab
    driver.switch_to.new_window("tab")
    current_handle = driver.current_window_handle
    logging.info(f"current handle: [{current_handle}]")

    handles = driver.window_handles
    for item in handles:
        logging.info(f"Windows handle: {item}")
        if item != current_handle:
            driver.switch_to.window(item)
            driver.close()

    driver.switch_to.window(current_handle)
    logging.info(f"current handle: [{driver.current_window_handle}]")

    wait(WAIT_TIME_5S)
    driver.maximize_window()
    
    yield driver
    logging.info("Browser is closing......")
    wait(WAIT_TIME_2S)
    try:
        driver.close()
        driver.quit()
    except Exception as e:
        logging.error(str(e))
    
    

@pytest.fixture()
def rp_logger(request):
    
    test_case_name = request.node.location[2]
    
    logger = logging.getLogger(test_case_name)
    logger.setLevel(logging.DEBUG)

    logging.info(os.path.abspath(__file__))
    logging.critical(request.node.config.args[0])
    
    log_file_path =os.path.join(root_dir, 'Logs', f'{test_case_name}.log') #os.path.dirname(os.path.abspath(__file__))
    # with open(log_file_path, "w") as fp:
    #     fp.seek(0)
    fileHandler = logging.FileHandler(log_file_path, mode="w")
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(filename)s [line:%(lineno)d] | %(message)s")
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    # logger.addHandler(RPLogHandler())
    logging.setLoggerClass(RPLogger)

    request.cls.rplogger = logger
    yield

@pytest.fixture(autouse=True)
def skip_by_mark(request):
    if request.node.get_closest_marker('fixture_skip'):
        pytest.skip('skip by fixture')

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when in ("setup", "call"):
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            time.sleep(1)
            test_case_name = item.location[2] #".".join(item.nodeid.split("::")[1:])
            screenshot_dir = os.path.join(root_dir, "Screenshots", get_dt("D"), test_case_name) #os.path.dirname(os.path.abspath(__file__))
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)
            # Take screenshot if there's still active driver
            if item is not None and item.cls is not None and item.cls.driver is not None:
                item.cls.driver.save_screenshot(os.path.join(screenshot_dir,"exception.png"))

@pytest.fixture()
def setup(request):
    with open(os.path.join(root_dir, "Config", "env.json"), mode="r") as fp:
        env_config = json.load(fp)

    browser_name = env_config["browser"]
    browser_version = env_config["version"]

    logging.info(f"Initiating {browser_name} driver")

    logging.info("clean existed screenshots")
    current_dt = get_dt("D")
    test_case_name = request.node.location[2] #".".join(request.node.nodeid.split("::")[1:])
    screenshots_dir = os.path.join(root_dir, "Screenshots", current_dt, test_case_name) #os.path.dirname(os.path.abspath(__file__))
    if os.path.exists(screenshots_dir):
        shutil.rmtree(screenshots_dir)

    if browser_name == "chrome":
        chrome_options = ChromeOptions()
        chrome_options.add_argument("start-maximized")
        # chrome_options.add_argument("--ignore-certificate-errors")
        # # chrome_options.add_argument("--incognito")
        # chrome_options.add_argument("--enable-automation")
        # chrome_options.add_argument("--no-sandbox")
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        chrome_options.add_experimental_option("useAutomationExtension", False)

        driver = webdriver.Chrome(service=ChromeService(executable_path="chromedriver.exe"), options= chrome_options)
        # if browser_version is not None:
        #     driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(driver_version=browser_version).install()))
        # else:
        #     driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    elif browser_name == "edge":
        edge_options = EdgeOptions()
        edge_options.add_argument("--start-maximized")
        edge_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        edge_options.add_experimental_option("useAutomationExtension", False)

        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install(), service_args=['--append-log', '--readable-timestamp', '--log-level=DEBUG'], log_output="testedge.log"))
        driver.maximize_window()
    elif browser_name == "firefox":
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    elif browser_name == "chromium":
        driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
    else:
        if browser_version is not None:
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(driver_version=browser_version).install()))
        else:
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    
    driver.implicitly_wait(WAIT_TIME_5S)
    
    request.cls.driver = driver

    # session = request.node
    # for item in session.items:
    #     cls = item.getparent(pytest.Class)
    #     setattr(cls.obj, "driver", driver)


    driver.switch_to.new_window("tab")
    current_handle = driver.current_window_handle
    print(f"current handle: [{current_handle}]")

    handles = driver.window_handles
    for item in handles:
        print(f"Windows handle: {item}")
        if item != current_handle:
            driver.switch_to.window(item)
            driver.close()

    driver.switch_to.window(current_handle)
    logging.info(f"current handle: [{driver.current_window_handle}]")

    driver.get("about:blank")
    time.sleep(1)
    
    # driver.maximize_window()
    yield driver
    wait(WAIT_TIME_2S)
    try:
        driver.close()
        driver.quit()
    except Exception as e:
        logging.error(str(e))
        logging.error(traceback.format_exc())
    # upload screenshots if screenshot name's preffix as same as test case name.
    upload_screenshots(screenshots_dir)
    # upload logs for individual test case
    logs_file_path = os.path.join(root_dir, "Logs", f"{test_case_name}.log")
    upload_logs_with_desc(logs_file_path)