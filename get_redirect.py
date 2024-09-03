import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time


# url = "https://login.microsoftonline.com/af8e89a3-d9ac-422f-ad06-cc4eb4214314/oauth2/v2.0/authorize?client_id=91698855-ba6e-4daf-b8bd-f441f269f570&response_type=id_token&redirect_uri=https://w4b.astrazeneca.net/auth/sso&response_mode=form_post&scope=openid&state=eyJyZXF1ZXN0ZWRfdXJsIjogImh0dHBzOi8vc2hpbnkuY29kZTEuYXN0cmF6ZW5lY2EubmV0L2FwcC9teWFwcC9sb2dpbiIsICJzdGF0ZSI6ICJ1cmk9L292ZXJ2aWV3In0=&nonce=678910"
# resp = requests.get(url, allow_redirects=True)

# print(resp.status_code)
# print(resp.headers)

# print(requests.head(url).headers)

# try:
#     while True:
#         long_url = requests.head(url).headers['location']
#         print(long_url)
#         url = long_url
# except:
#     print(long_url)


def get_redirect_url():
    url = "https://uwhwls33a0.execute-api.cn-north-1.amazonaws.com.cn/dev/auth/sso/get-sso-url"

    params = {
        "state": "uri=/overview",
        "requested_url": "https://shiny.code1.astrazeneca.net/app/myapp/login"
    }

    response = requests.request("GET", url, params=params)

    json_resp = json.loads(response.text)
    return json_resp["headers"]["Location"] if json_resp["statusCode"] == 302 else None


def get_chrome_token(url):

    chrome_options = ChromeOptions()
    chrome_options.add_argument("start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

    driver = webdriver.Chrome(service=ChromeService(executable_path="chromedriver.exe"), options= chrome_options)
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
    time.sleep(10)
    driver.get(url)
    time.sleep(60)

    # scriptToExecute = "var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return JSON.stringify(network);";
    # data = driver.execute_script(scriptToExecute)
    # print(data)

    def process_browser_log_entry(entry):
        response = json.loads(entry['message'])['message']
        return response

    browser_log = driver.get_log('performance')
    with open("chromelog.txt", mode="w") as fp:
        fp.write(json.dumps(browser_log, indent=4))

    # events = [process_browser_log_entry(entry) for entry in browser_log]
    # print(json.dumps(events))
    # events = [event for event in events if 'Network.response' in event['method']]
    # print(events)

def get_id_token():
    url = "https://login.microsoftonline.com/af8e89a3-d9ac-422f-ad06-cc4eb4214314/oauth2/v2.0/authorize"

    params = {
        "client_id":"91698855-ba6e-4daf-b8bd-f441f269f570",
        "response_type":"id_token",
        "redirect_uri":"https://w4b.astrazeneca.net/auth/sso",
        "response_mode":"form_post",
        "scope":"openid",
        "state":"eyJyZXF1ZXN0ZWRfdXJsIjogImh0dHBzOi8vc2hpbnkuY29kZTEuYXN0cmF6ZW5lY2EubmV0L2FwcC9teWFwcC9sb2dpbiIsICJzdGF0ZSI6ICJ1cmk9L292ZXJ2aWV3In0=",
        "nonce":678910,
        "sso_reload":"true"
    }

    headers = {
        'Authorization': 'Basic a3R2ajk0M0Bhc3RyYXplbmVjYS5uZXQ6UWF6ITEzNTI0Ng=='
    }

    s = requests.Session()

    response = s.get(url, headers=headers, params=params, allow_redirects=True)
    print(response.status_code)
    print(response.text)
    # response2 = s.head("https://w4b.astrazeneca.net/auth/sso")
    # print(response2.headers)
    

# get_id_token()

redirect_url = get_redirect_url()
print(redirect_url)

get_chrome_token(redirect_url)