import requests

import json

class ApiRequest:

    @staticmethod
    def get(url, headers={}, parameters={}, expected_code=200):
        res = requests.request("GET", url, headers=headers, params=parameters)
        res.encoding = res.apparent_encoding
        if res.status_code == expected_code:
            result = json.loads(res.text)
            return result
        else:
            raise Exception(f"Get Request with exception, returned code: <<{res.status_code}>>")
        
    @staticmethod
    def post(url, headers={}, parameters={}, body={}, expected_code=200):
        res = requests.post(url, headers=headers, data=body, params=parameters)
        res.encoding = res.apparent_encoding
        if res.status_code == expected_code:
            result = json.loads(res.text)
            return result
        else:
            raise Exception(f"Post Request with exception, returned code: <<{res.status_code}>>")



payload = {
    "key1": "value2",
    "key2": ["value2", "value3"]
    }

res = ApiRequest.get("https://httpbin.org/get", parameters=payload)
print(res)

# r = requests.get("https://api.github.com/events", stream=True)
# with open("mygithubEvents.json", 'w') as fp:
#     json.dump(json.loads(r.text), fp, indent=4)
parameters = {
    "param1": "paramvalue1"
}

payload_tuples = [("key1", "value1"), ("key2", "value2")]

payload_dict = {"key1": ["value1", "value2"]}
res_post = ApiRequest.post("https://httpbin.org/post", parameters=parameters, body=payload_dict)
print(res_post)

# r = requests.get("https://kyfw.12306.cn/otn/", verify=True)
# print(r.text)

bad_r = requests.get("https://httpbin.org/status/404")
print(bad_r.status_code)
bad_r.raise_for_status()
