import logging
from time import sleep
import subprocess
import os
from datetime import datetime
from Screenshot import Screenshot


WAIT_TIME_1S   = 1
WAIT_TIME_2S   = 2
WAIT_TIME_5S   = 5
WAIT_TIME_10S  = 10
WAIT_TIME_20S  = 20
WAIT_TIME_30S  = 30
WAIT_TIME_60S  = 60
WAIT_TIME_120S = 120
WAIT_TIME_150S = 150

def start_browser(lock, browser_type, browser_port):
    lock.acquire()
    subprocess.run(f"start_{browser_type}_{browser_port}.bat")
    wait(WAIT_TIME_2S, "release locked browser")
    lock.release()


def wait(s, message="Wait time count Down"):
    logging.info(f"Will wait for <{s}> seconds!!!")
    if s>=1:
        while s>0:
            logging.debug(f"{message}: {s}")
            sleep(1)
            s-=1
    else:
        sleep(s)

def generate_start_chrome(browser_port):
    chrome_path = '"C:\Program Files\Google\Chrome\Application\chrome.exe"'
    chrome_data = f'--user-data-dir="C:\\temp\{str(browser_port)}"'
    chrome_port = f'--remote-debugging-port={browser_port}'
    config_str = f"{chrome_path} {chrome_port} {chrome_data}"
    if not os.path.exists(os.path.join(os.getcwd(), f"start_chrome_{browser_port}.bat")):
        with open(f"start_chrome_{browser_port}.bat", mode="w") as fp:
            fp.write(config_str)

def get_dt(category="F"):
    """
    format category: 
    1. Full Datetime: "%Y%m%d%H%M%S"
    2: Date: "%Y%m%d"
    3: Time: "%H%M%S"
    4: Hour: "%Y%m%d%H"
    """
    category = category.upper()
    if category == "F":
        format = "%Y%m%d%H%M%S"
    elif category == "D":
        format = "%Y%m%d"
    elif category == "T":
        format = "%H%M%S"
    elif category == "H":
        format = "%Y%m%d%H"
    else:
        format = "%Y%m%d%H%M%S"
    return datetime.now().strftime(format)

def upload_screenshots(dir_path):
    if os.path.exists(dir_path):
        screenshot_list = sorted(os.listdir(dir_path), key=lambda x: os.path.getmtime(os.path.join(dir_path, x)))
        for single_file in screenshot_list:
            if os.path.splitext(single_file)[1].upper() == ".PNG":
                screenshot_file_path = os.path.join(dir_path, single_file)
                with open(screenshot_file_path, "rb") as image_file:
                    file_data = image_file.read()
                    # noinspection PyArgumentList
                    logging.info(
                        f"Screenshot attached: [{single_file}]",
                        attachment={
                            "name": single_file,
                            "data": file_data,
                            "mime": "image/png"
                        }
                    )
    else:
        logging.debug(f"The path: [{dir_path}] not exists, plz re-check!")

def upload_screenshot_with_desc(file_path, desc=""):    
    if os.path.exists(file_path) and os.path.splitext(file_path)[1].upper() == ".PNG":
        file_name = os.path.basename(file_path)
        with open(file_path, "rb") as image_file:
            file_data = image_file.read()
            # noinspection PyArgumentList
            logging.info(
                f"Screenshot attached: [{file_name}]" if desc=="" else f"{desc}: [{file_name}]",
                attachment={
                    "name": file_name,
                    "data": file_data,
                    "mime": "image/png"
                }
            )

def upload_logs_with_desc(file_path, desc=""):    
    if os.path.exists(file_path) and os.path.splitext(file_path)[1].upper() == ".LOG":
        file_name = os.path.basename(file_path)
        with open(file_path, "rb") as image_file:
            file_data = image_file.read()
            # noinspection PyArgumentList
            logging.info(
                f"Logs attached: [{file_name}]" if desc=="" else f"{desc}: [{file_name}]",
                attachment={
                    "name": file_name,
                    "data": file_data,
                    "mime": "text/plain"
                }
            )