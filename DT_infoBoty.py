#!/usr/bin/env python
# -*- coding:utf-8 -*-

import discord
import json
from TeaShop import runLoki
from ArticutAPI import Articut

numberDICT={"一":1,"二":2,"三":3,"四":4,"五":5,"六":6,"七":7,"八":8,"九":9,"十":10}

with open("account.info", encoding="utf-8") as f:
    accountDICT = json.loads(f.read())

class BotClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {} with id {}'.format(self.user, self.user.id))

    async def on_message(self, message):
        # Don't respond to bot itself. Or it would create a non-stop loop.
        # 如果訊息來自 bot 自己，就不要處理，直接回覆 None。不然會 Bot 會自問自答個不停。
        if message.author == self.user:
            return None

        print("到到來自 {} 的訊息".format(message.author))
        print("訊息內容是 {}。".format(message.content))
        if self.user.mentioned_in(message):
            print("本 bot 被叫到了！")
            msg = message.content.replace("<@!{}> ".format(self.user.id), "")
            if msg == 'ping':
                await message.reply('pong')
            elif msg == 'ping ping':
                await message.reply('pong pong')
            else:
                articut = Articut(username=accountDICT["username"], apikey=accountDICT["apikey"])
                responseSTR = "我是預設的回應字串…你會看到我這串字，肯定是出了什麼錯！"
                inputLIST = [msg]
                filterLIST = []
                resultDICT = runLoki(inputLIST, filterLIST)
                
                amount=[]
                for n in range(0,len(resultDICT['amount'])):
                    if type(resultDICT['amount'][n]) == int:
                        amount=resultDICT["amount"]
                    else:
                        articutLv3ResultDICT = articut.parse(resultDICT["amount"][n], level="lv3")
                        amount.append(articutLv3ResultDICT["number"][resultDICT["amount"][n]])


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
          

                responseSTR='您點的是：'
                for n in range(0,len(resultDICT['amount'])):
                    responseSTR=responseSTR+f'{amount[n]}杯 {item[n]}，尺寸是 {size[n]}，甜度是 {sugar[n]}，冰塊是 {ice[n]} 的 {temperature[n]}。\n'
                    n+=1
                responseSTR=responseSTR+'謝謝您的光臨~~'
                await message.reply(responseSTR)
            

if __name__ == "__main__":
    client = BotClient()
    client.run(accountDICT["discord_token"])