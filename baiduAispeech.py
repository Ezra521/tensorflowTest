# from aip import AipSpeech
#
# """ 你的 APPID AK SK """
# APP_ID = '10901448'
# API_KEY = 'xOxHqIPs6s2Un2Nn2rihv8e4'
# SECRET_KEY = 'II2p5MF2HnYkH7ZE29WsQ1swyGuC9d63'
#
# client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

#!/usr/bin/env python
# coding: utf-8
import urllib2
import json
import base64
import  os

#设置应用信息
baidu_server = "https://openapi.baidu.com/oauth/2.0/token?"
grant_type = "client_credentials"
client_id = "SrhYKqzl3SE1URnAEuZ0FKdT" #填写API Key
client_secret = "hGqeCkaMPb0ELMqtRGc2VjWdmjo7T89d" #填写Secret Key

#合成请求token的URL
url = baidu_server+"grant_type="+grant_type+"&client_id="+client_id+"&client_secret="+client_secret

#获取token
res = urllib2.urlopen(url).read()
data = json.loads(res)
token = data["access_token"]
print token

#设置音频属性，根据百度的要求，采样率必须为8000，压缩格式支持pcm（不压缩）、wav、opus、speex、amr
VOICE_RATE = 16000
WAVE_FILE ="F://python//a.pcm" #音频文件的路径
USER_ID = "hail_hydra" #用于标识的ID，可以随意设置
WAVE_TYPE = "wav"

#打开音频文件，并进行编码
f = open(WAVE_FILE, "r")
speech = base64.b64encode(f.read())
size = os.path.getsize(WAVE_FILE)
update = json.dumps({"format":WAVE_TYPE, "rate":VOICE_RATE, 'channel':1,'cuid':USER_ID,'token':token,'speech':speech,'len':size})
headers = { 'Content-Type' : 'application/json' }
url = "http://vop.baidu.com/server_api"
req = urllib2.Request(url, update, headers)

r = urllib2.urlopen(req)


t = r.read()
print t
result = json.loads(t)
print result
if result['err_msg']=='success.':
    word = result['result'][0].encode('utf-8')
    if word!='':
        if word[len(word)-3:len(word)]=='，':
            print word[0:len(word)-3]
        else:
            print word
    else:
        print "wav format error"
else:
    print "error %s" % result['err_msg']