# -*- coding: utf-8 -*-
import urllib
import urllib2
import httplib
import random
import md5
import time
import hashlib
import re
import os
import string
import json
import sys
import time
# reload(sys)
# sys.setdefaultencoding("utf-8")
# from translate import Translator
rootdir = 'src'
rootdir2='resource/skins'
appid = '20191016000341854' #你的appid
secretKey = '403rVIIxGO72XLX7GOj4' #你的密钥
def bianli(strr):
    list = os.listdir(strr)
    for i in range(0,len(list)):
        path = os.path.join(strr,list[i])
        dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        #print path
        if os.path.isfile(path):
            if (".ts" in path)or(".exml" in path):
                print("==============="+dir_path+path+"===============")
                w_str=""
                fopen=open(path,'r+')
                # for line in fopen:
                #     w_str+=line
                w_str = fopen.read()
                line = w_str.strip().decode('utf-8', 'ignore')  # 处理前进行相关的处理，包括转换成Unicode等
                p2 = re.compile(ur'[^\u4e00-\u9fa5]')  # 中文的编码范围是：\u4e00到\u9fa5
                zh = " ".join(p2.split(line)).strip()
                zh = ",".join(zh.split())
                paramArray=zh.split(",")
                for each in paramArray:
                    if not each:
                        continue
                    newParams=""
                    # print(stop)
                    if stop==0:
                        # newParams=request(each)
                        time.sleep(0.1)
                        newParams=baiduTR(each)
                        print(newParams)
                    elif stop==1:
                        # newParams=baidu_translate(each,1)
                        time.sleep(1)
                        newParams=baiduTR(each)
                    elif stop==2:
                        time.sleep(1)
                        newParams=baiduTR(each)
                    # print(paramsA[num])
                    oldParams=each.encode('utf-8')
                    w_str= w_str.replace(oldParams,newParams.encode('utf-8'),1)
                fopen.seek(0)#文件定位到position 0
                fopen.truncate()#清空文件
                fopen.write(w_str)
                fopen.close()
        else:
            bianli(path)

# 百度翻译
def baiduTR(strr):
    print(strr)
    httpClient = None
    myurl = '/api/trans/vip/translate'
    q = strr.encode('utf-8')
    fromLang = 'zh'
    toLang = 'en'
    salt = random.randint(32768, 65536)

    sign = appid+q+str(salt)+secretKey
    m1 = md5.new()
    m1.update(sign)
    sign = m1.hexdigest()
    myurl = myurl+'?appid='+appid+'&q='+urllib.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
    translate_result=""
    # try:
    httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
    httpClient.request('POST', myurl)
     
        #response是HTTPResponse对象
    response = httpClient.getresponse()
    result=response.read()
    try:
        resultA=json.loads(result)
        translate_result = resultA['trans_result'][0]['dst']
    except:
        print(result)
    return translate_result
# 有道翻译
def request(strr):
    print(strr)
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
    keyword = strr.encode('utf-8')
    headers = {
    # "Accept": "application/json, text/javascript, */*; q=0.01",
    # "Connection": "keep-alive",
    # "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "1677583082@118.186.227.36",
    "Referer": "http://fanyi.youdao.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
    # "X-Requested-With": "XMLHttpRequest",
    }
    paramsInt=int(time.time()*1000)
    salt = '%d'%paramsInt

    m = hashlib.md5()
    strl = "fanyideskweb" + keyword + salt + "ebSeFb%=XZ%T[KZ)c(sy!"
    m.update(strl)
    sign = m.hexdigest().encode('utf-8')
    data = {
        "i":keyword,
        "from":"zh",
        "to":"en",
        "smartresult":"dict",
        "client":"fanyideskweb",
        "salt":salt,
        "sign":sign,
        "doctype":"json",
        "version":"2.1",
        "keyfrom":"fanyi.web",
        "action":"FY_BY_REALTIME",
        "typoResult":"false"
    }
    data = urllib.urlencode(data)
    request = urllib2.Request(url,data=data,headers=headers)
    response = urllib2.urlopen(request)
    result=response.read()
    resultA = ""
    try:
        resultA=json.loads(result)
    except:
        print("翻译次数上线")
        global stop
        stop=1
        # print(result)
        # if stop:
        #     sys.exit(0)
    # print(resultA)
    translate_result = ""
    try:
        translate_result = resultA['translateResult'][0][0]['tgt']
    except:
        print(resultA)
    return translate_result
    # print(translate_result)
    # print(type(translate_result[0][0]))
    # print(translate_result[0][0]['tgt'])
	# print(translate_result.encode('utf-8'))


# def baidu_translate(content,type=1):
#     print(content+"aa")
#     # print("--------------处理中-----------------")
#     translator = Translator(from_lang="chinese",to_lang="english")
#     translation = translator.translate(content)
#     return translation
stop=0
bianli(rootdir)
# bianli(rootdir2)



