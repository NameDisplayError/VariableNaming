import hashlib
import random
import re
from configparser import ConfigParser
from string import punctuation, digits
import pyperclip
import requests

from wox import Wox


def config():
    cof = ConfigParser()
    cof.read('config.ini')
    return dict(cof.items('translate'))


url = "https://fanyi-api.baidu.com/api/trans/vip/translate"

app_id = ""

key = ""

frompara = "zh"

to = "en"


class Main(Wox):

    # query is default function to receive realtime keystrokes from wox launcher
    def query(self, query):
        res = translate(query)
        res = res.lower()
        res = processing_symbols(res)
        snake = to_snake(res)
        upper = to_upper(res)
        lower = upper[0].lower() + upper[1:]
        results = [{
            "Title": f"{upper}",
            "SubTitle": "大驼峰",
            "IcoPath": "Images/app.png",
            "ContextData": "ctxData",
            "JsonRPCAction": {
                'method': 'take_action',
                'parameters': ["{}".format(upper)],
                'dontHideAfterAction': False
            }
        }, {
            "Title": f"{lower}",
            "SubTitle": "小驼峰",
            "IcoPath": "Images/app.png",
            "ContextData": "ctxData",
            "JsonRPCAction": {
                'method': 'take_action',
                'parameters': ["{}".format(lower)],
                'dontHideAfterAction': False
            }
        }
        ]
        if snake != lower:
            results.append({
                "Title": f"{snake}",
                "SubTitle": "蛇形",
                "IcoPath": "Images/app.png",
                "ContextData": "ctxData",
                "JsonRPCAction": {
                    'method': 'take_action',
                    'parameters': ["{}".format(snake)],
                    'dontHideAfterAction': False
                }
            })
        return results

    # context_menu is default function called for ContextData where `data = ctxData`
    def context_menu(self, data):
        results = [{
            "Title": "Context menu entry",
            "SubTitle": "Data: {}".format(data),
            "IcoPath": "Images/app.png"
        }]
        return results

    def take_action(self, someArgument):
        # Choose what to trigger on pressing enter on the result.
        # use SomeArgument to do something with data sent by parameters.
        pyperclip.copy(str(someArgument))


def processing_symbols(q: str) -> str:
    return re.sub(r'[^0-9a-zA-Z]+', ' ', q)


def translate(q: str) -> str:
    salt = random.Random().randint(0, 1000000)

    sign_para = sign(app_id, q, salt, key)

    temp_url = url + f"?q={q}&from={frompara}&to={to}&appid={app_id}&salt={salt}&sign={sign_para}"

    resp = requests.get(temp_url).json()

    return resp["trans_result"][0]['dst']


def to_upper(str_para: str):
    res = ''
    for i in str_para.lower().split(' '):
        res += i.capitalize()
    return res


def to_snake(str_para: str):
    return re.sub(r' +', '_', str_para)


def sign(appid, query, salt, keyword) -> str:
    return hashlib.md5((appid + query + str(salt) + keyword).encode("utf-8")).hexdigest().lower()


if __name__ == '__main__':
    Main()
