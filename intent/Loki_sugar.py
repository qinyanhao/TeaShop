#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for sugar

    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict

    Output:
        resultDICT    dict
"""

DEBUG_sugar = True
userDefinedDICT = {"hot": ["常溫", "溫飲", "熱飲", "燙"], "ice": ["去冰", "微冰", "少冰", "半冰", "全冰", "微微", "正常冰", "一分冰", "二分冰", "五分冰", "冰塊", "完全去冰"], "size": ["大", "中", "小"], "sugar": ["無糖", "微糖", "少糖", "半糖", "全糖", "微微", "正常糖", "糖"], "原鄉四季": ["原鄉四季", "四季", "四季春", "原鄉", "四季茶", "四季春茶", "原鄉茶", "原鄉四季茶", "原鄉四季春茶", "原鄉四季春茶", "四季原鄉"], "極品菁茶": ["極品菁茶", "極品菁", "菁茶", "極菁", "極菁茶"], "烏龍綠茶": ["烏龍綠茶", "烏龍", "烏龍綠", "烏"], "特級綠茶": ["特級綠茶", "綠茶", "綠", "特綠"], "特選普洱": ["特選普洱", "特選普洱茶", "普洱", "普洱茶", "特普", "特級普洱茶", "特級普洱"], "翡翠烏龍": ["翡翠烏龍", "翡翠烏", "翡翠烏龍茶", "翡翠烏茶", "翡翠烏龍綠", "翡翠烏綠", "翠烏", "翠烏茶", "翡烏", "翡烏茶", "烏龍"], "錫蘭紅茶": ["錫蘭紅茶", "錫蘭", "錫蘭紅", "紅茶", "錫茶", "蘭茶", "紅"], "嚴選高山茶": ["嚴選高山茶", "高山", "高山茶", "嚴選高山", "嚴選高"]}

sugarDICT= {'0分':'無糖','兩分':'微糖','五分':'半糖','八分':'少糖', '正常':'全糖'}
# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_sugar:
        print("[sugar] {} ===> {}".format(inputSTR, utterance))

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    resultDICT['sugar']=[]
    
    if utterance == "[一杯][大]冰[綠][半糖][少冰]":
        if args[3] in userDefinedDICT["sugar"]:
            resultDICT["sugar"].append(args[3])
        elif args[4] in userDefinedDICT["sugar"]:
            resultDICT["sugar"].append(args[4])
        else:
            pass

    if utterance == "[原鄉][兩杯]，[一杯][半糖][少冰]，[一杯][全糖][正常冰]": 
        if args[4]  in userDefinedDICT["sugar"]:
            resultDICT["sugar"].append(args[4])
        elif args[3] in userDefinedDICT["sugar"]:
            resultDICT["sugar"].append(args[3])
        else:
            pass
        if args[7]  in userDefinedDICT["sugar"]:
            resultDICT["sugar"].append(args[7])
        elif args[6] in userDefinedDICT["sugar"]:
            resultDICT["sugar"].append(args[6])
        else:
            pass

    if utterance == "[嚴選高山茶][兩分][糖][大]杯[少冰]":
        if args[1] in sugarDICT.keys():
            resultDICT["sugar"].append(sugarDICT[args[1]])
        else:
            pass

    if utterance == "[我]要[菁茶]，[半糖]不要[冰塊]":
        if args[2] in userDefinedDICT["sugar"]:
            resultDICT["sugar"].append(args[2])
        elif args[3] in userDefinedDICT["sugar"]:
            resultDICT["sugar"].append(args[3])
        else:
            pass

    if utterance == "普洱[微微]":
        resultDICT["sugar"].append('微糖')
        

    if utterance == "[嚴選高山茶][微糖][大]杯[少冰]":
        if args[1] in userDefinedDICT["sugar"]:
            resultDICT["sugar"].append(args[1])
        elif args[3] in userDefinedDICT["sugar"]:
            resultDICT["sugar"].append(args[3])
        else:
            pass
        
    if utterance == "[我]要[一杯][錫蘭紅茶][溫]的":
        resultDICT["sugar"].append('全糖')

    if utterance == "[3杯][綠茶]，[甜度][冰塊][都][正常]":
        if args[5] in sugarDICT.keys():
            resultDICT['sugar'].append(sugarDICT[args[5]])
            
        else:
            pass
        
    if utterance == "[一杯][小][溫][紅]，[微糖]":
        if args[4] in userDefinedDICT["sugar"]:
            resultDICT["sugar"].append(args[4])
        else:
            pass

    if utterance == "[一杯][菁茶]，[一杯][高山]": 
        resultDICT["sugar"].append('全糖')
        resultDICT["sugar"].append('全糖')

    if utterance == "[兩杯][熱]的[錫蘭紅茶][甜度][冰塊][正常]":
        if args[5] in sugarDICT.keys():
            resultDICT['sugar'].append(sugarDICT[args[5]])
        else:
            pass

    if utterance == "[我]要[兩杯]飲料，[一杯][菁茶][微糖][微冰]，[一杯][高山][半糖][少冰]": 
        if args[4]  in userDefinedDICT["sugar"]:
            resultDICT["sugar"].append(args[4])
        elif args[5] in userDefinedDICT["sugar"]:
            resultDICT["sugar"].append(args[5])
        else:
            pass
        if args[8]  in userDefinedDICT["sugar"]:
            resultDICT["sugar"].append(args[8])
        elif args[9] in userDefinedDICT["sugar"]:
            resultDICT["sugar"].append(args[9])
        else:
            pass

    return resultDICT