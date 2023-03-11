import requests
import os

def main(
    my_value: str
):
    headers={'Authorization': "Bearer: {}".format(os.environ.get("WM_USERNAME"))}
    r = requests.post('https://httpbin.org/post', headers=headers, data={'key': my_value})
    return r.json()
