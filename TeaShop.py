#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki 2.0 Template For Python3

    [URL] https://api.droidtown.co/Loki/BulkAPI/

    Request:
        {
            "username": "your_username",
            "input_list": ["your_input_1", "your_input_2"],
            "loki_key": "your_loki_key",
            "filter_list": ["intent_filter_list"] # optional
        }

    Response:
        {
            "status": True,
            "msg": "Success!",
            "version": "v223",
            "word_count_balance": 2000,
            "result_list": [
                {
                    "status": True,
                    "msg": "Success!",
                    "results": [
                        {
                            "intent": "intentName",
                            "pattern": "matchPattern",
                            "utterance": "matchUtterance",
                            "argument": ["arg1", "arg2", ... "argN"]
                        },
                        ...
                    ]
                },
                {
                    "status": False,
                    "msg": "No Match Intent!"
                }
            ]
        }
"""

from requests import post
from requests import codes
import math
try:
    from intent import Loki_sugar
    from intent import Loki_item
    from intent import Loki_ice
    from intent import Loki_size
    from intent import Loki_temperature
except:
    from .intent import Loki_sugar
    from .intent import Loki_item
    from .intent import Loki_ice
    from .intent import Loki_size
    from .intent import Loki_temperature

from ArticutAPI import Articut
import json
with open("account.info", encoding="utf-8") as f:
    accountDICT = json.loads(f.read())

LOKI_URL = "https://api.droidtown.co/Loki/BulkAPI/"
USERNAME = accountDICT["username"]
LOKI_KEY = accountDICT["lokikey"]
# 意圖過濾器說明
# INTENT_FILTER = []        => 比對全部的意圖 (預設)
# INTENT_FILTER = [intentN] => 僅比對 INTENT_FILTER 內的意圖
INTENT_FILTER = []

class LokiResult():
    status = False
    message = ""
    version = ""
    balance = -1
    lokiResultLIST = []

    def __init__(self, inputLIST, filterLIST):
        self.status = False
        self.message = ""
        self.version = ""
        self.balance = -1
        self.lokiResultLIST = []
        # filterLIST 空的就採用預設的 INTENT_FILTER
        if filterLIST == []:
            filterLIST = INTENT_FILTER

        try:
            result = post(LOKI_URL, json={
                "username": USERNAME,
                "input_list": inputLIST,
                "loki_key": LOKI_KEY,
                "filter_list": filterLIST
            })

            if result.status_code == codes.ok:
                result = result.json()
                self.status = result["status"]
                self.message = result["msg"]
                if result["status"]:
                    self.version = result["version"]
                    self.balance = result["word_count_balance"]
                    self.lokiResultLIST = result["result_list"]
            else:
                self.message = "Connect failed."
        except Exception as e:
            self.message = str(e)

    def getStatus(self):
        return self.status

    def getMessage(self):
        return self.message

    def getVersion(self):
        return self.version

    def getBalance(self):
        return self.balance

    def getLokiStatus(self, index):
        rst = False
        if index < len(self.lokiResultLIST):
            rst = self.lokiResultLIST[index]["status"]
        return rst

    def getLokiMessage(self, index):
        rst = ""
        if index < len(self.lokiResultLIST):
            rst = self.lokiResultLIST[index]["msg"]
        return rst

    def getLokiLen(self, index):
        rst = 0
        if index < len(self.lokiResultLIST):
            if self.lokiResultLIST[index]["status"]:
                rst = len(self.lokiResultLIST[index]["results"])
        return rst

    def getLokiResult(self, index, resultIndex):
        lokiResultDICT = None
        if resultIndex < self.getLokiLen(index):
            lokiResultDICT = self.lokiResultLIST[index]["results"][resultIndex]
        return lokiResultDICT

    def getIntent(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["intent"]
        return rst

    def getPattern(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["pattern"]
        return rst

    def getUtterance(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["utterance"]
        return rst

    def getArgs(self, index, resultIndex):
        rst = []
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["argument"]
        return rst

def runLoki(inputLIST, filterLIST=[]):
    resultDICT = {}
    lokiRst = LokiResult(inputLIST, filterLIST)
    if lokiRst.getStatus():
        for index, key in enumerate(inputLIST):
            for resultIndex in range(0, lokiRst.getLokiLen(index)):
                # sugar
                if lokiRst.getIntent(index, resultIndex) == "sugar":
                    resultDICT = Loki_sugar.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # item
                if lokiRst.getIntent(index, resultIndex) == "item":
                    resultDICT = Loki_item.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # ice
                if lokiRst.getIntent(index, resultIndex) == "ice":
                    resultDICT = Loki_ice.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # size
                if lokiRst.getIntent(index, resultIndex) == "size":
                    resultDICT = Loki_size.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # temperature
                if lokiRst.getIntent(index, resultIndex) == "temperature":
                    resultDICT = Loki_temperature.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

    else:
        resultDICT = {"msg": lokiRst.getMessage()}
    return resultDICT

def testLoki(inputLIST, filterLIST):
    INPUT_LIMIT = 20
    for i in range(0, math.ceil(len(inputLIST) / INPUT_LIMIT)):
        resultDICT = runLoki(inputLIST[i*INPUT_LIMIT:(i+1)*INPUT_LIMIT], filterLIST)

    
def printResult():
    print('您點的是：')
    for n in range(0,len(resultDICT['amount'])):
        print(f'{amount[n]}杯 {item[n]}，尺寸是 {size[n]}，甜度是 {sugar[n]}，冰塊是 {ice[n]} 的 {temperature[n]}。')
        n+=1
   


if __name__ == "__main__":
    # sugar
    # print("[TEST] sugar")
    # inputLIST = ['普洱微微','一杯大冰綠半糖少冰','我要菁茶，半糖不要冰塊','嚴選高山茶兩分糖大杯少冰','原鄉兩杯，一杯半糖少冰，一杯全糖正常冰']
    # testLoki(inputLIST, ['sugar'])
    # print("")

    # item
    # print("[TEST] item")
    # inputLIST = ['普洱微微','一杯大冰綠半糖少冰','我要菁茶，半糖不要冰塊','嚴選高山茶兩分糖大杯少冰','原鄉兩杯，一杯半糖少冰，一杯全糖正常冰']
    # testLoki(inputLIST, ['item'])
    # print("")

    # ice
    # print("[TEST] ice")
    # inputLIST = ['普洱微微','一杯大冰綠半糖少冰','我要菁茶，半糖不要冰塊','嚴選高山茶兩分糖大杯少冰','原鄉兩杯，一杯半糖少冰，一杯全糖正常冰']
    # testLoki(inputLIST, ['ice'])
    # print("")

    # size
    # print("[TEST] size")
    # inputLIST = ['普洱微微','一杯大冰綠半糖少冰','我要菁茶，半糖不要冰塊','嚴選高山茶兩分糖大杯少冰','原鄉兩杯，一杯半糖少冰，一杯全糖正常冰']
    # testLoki(inputLIST, ['size'])
    # print("")

    # temperature
    # print("[TEST] temperature")
    # inputLIST = ['普洱微微','一杯大冰綠半糖少冰','我要一杯錫蘭紅茶溫的','我要菁茶，半糖不要冰塊','嚴選高山茶兩分糖大杯少冰','原鄉兩杯，一杯半糖少冰，一杯全糖正常冰']
    # testLoki(inputLIST, ['temperature'])
    # print("")

    articut = Articut(username=accountDICT["username"], apikey=accountDICT["apikey"])
    # 輸入其它句子試看看
    inputLIST = ["兩杯溫的錫蘭紅茶，甜度冰塊正常"]
    filterLIST = []
    resultDICT = runLoki(inputLIST, filterLIST)
    amount=[]
    
    for n in range(0,len(resultDICT['amount'])):
        if type(resultDICT["amount"][n]) == int:
            amount=resultDICT["amount"]
        else:
            articutLv3ResultDICT = articut.parse(resultDICT["amount"][n], level="lv3")
            amount.append(articutLv3ResultDICT["number"][resultDICT["amount"][n]])
    
    print("Result => {}".format(resultDICT))
    

    ice=[]
    temperature=[]
    for n in range(0,len(resultDICT['ice'])):
        if resultDICT['ice'][n] != None:
            ice=resultDICT['ice']
        else:
            ice.append('無')
   

    for n in range(0,len(resultDICT['temperature'])):
        if resultDICT['temperature'][n] != None:
           temperature=resultDICT['temperature']
        else:
            temperature.append('冷飲')
    
    item=resultDICT['item']
    size=resultDICT['size']
    sugar=resultDICT['sugar']
          
    print()
    printResult()
    
            
            
            