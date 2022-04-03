from Crypto.Cipher import DES3   
from Crypto.Util.Padding import pad, unpad
from tokenize import group
from urllib.parse import urlencode
import base64
import hashlib
import json
import os
import requests
import sys
import time

deviceKey = "ourHardworkByTheseWordsGuardedPleaseDontSteal(C)DICOT"
fileName = "dicli.conf"
comid = "100"
comkey = "8919244ff15d441bae4b944b112a33ea"
screctkey = "f1cd9351930d4e589922edbcf3b09a7c"
ts = str(int(time.time()))
urlEU = "http://api.eu.v-box.net/box-data/api/we-data/login"
urlBoxs = "http://api.eu.v-box.net/box-data/api/we-data/boxs"
urlGroups = "http://api.eu.v-box.net/box-data/api/we-data/realgroups"
urlConfig = "http://api.eu.v-box.net/box-data/api/we-data/realcfgs"

def hashKey(key):
    return hashlib.md5(bytes(key, encoding='utf8'))

def encrypt(message, unhashedKey):
    key = hashKey(unhashedKey)
    cipher = DES3.new(key.digest(), DES3.MODE_ECB)
    cipherText = cipher.encrypt(pad(message.encode('UTF8'), 8, style='pkcs7'))
    encryptedText = base64.b64encode(cipherText).decode('utf8')
    return encryptedText

def decrypt(message, unhashedKey):
    key = hashKey(unhashedKey)
    decipher = DES3.new(key.digest(), DES3.MODE_ECB)
    decipheredText = decipher.decrypt(base64.b64decode(message.encode('utf8')))
    decryptedText = unpad(decipheredText, 8, style='pkcs7').decode('UTF8')
    return decryptedText

def loginError():
    print("\n[error while logging in! exiting...]\n")
    sys.exit(1)

print("[welcome to dicli! initiating login process...]\n")

alias = input("[alias]: ")
pUnhashed = input("[password]: ")
pHashed = hashlib.md5(pUnhashed.encode())

urlParams = { 'alias': alias, 'password': pHashed.hexdigest() }
payload = { 'alias': alias, 'comid': comid, 'compvtkey': comkey, 'password': pHashed.hexdigest(), 'ts': ts, 'key': screctkey }
signUnhashed = urlencode(payload)
signHashed = hashlib.md5(signUnhashed.encode())
common = { 'compvtkey': comkey, 'sign': signHashed.hexdigest(), 'comid': comid, 'ts': ts }
commonHeader = {'common': str(common)}

print("\n[attempting login...]")
configFile = open(fileName, "w")
r = requests.post(urlEU, params=urlParams, headers=commonHeader)
if(r.status_code == 200):
    configFile.write(encrypt(r.text, deviceKey))
    configFile.close()
    print("[succesfully logged in! fetching boxes list...]\n")
else:
    configFile.close()
    loginError()

rjson = r.json()
payloadBoxs = { 'comid': comid, 'compvtkey': comkey, 'sid': rjson["result"]["sid"], 'ts': ts, 'key': screctkey }
boxsUnhashed = urlencode(payloadBoxs)
boxsSign = hashlib.md5(boxsUnhashed.encode())
headerBoxs = { 'sid': rjson["result"]["sid"], 'comid': comid, 'compvtkey': comkey, 'ts': ts, 'sign': boxsSign.hexdigest() }
commonBoxs = { 'common': str(headerBoxs) }

rBoxs = requests.post(urlBoxs, headers=commonBoxs)
configFile = open(fileName, "a")
configFile.write(encrypt(rBoxs.text, deviceKey))
configFile.close()
boxsJson = rBoxs.json()
finalJson = boxsJson["result"]

print("[the following boxes were detected]")
for box in finalJson["list"]:
    print("\t", box["boxList"][0]["boxName"], box["boxList"][0]["boxId"])
boxId = input("[enter your desired boxid]: ")
groupParams = { 'boxId': boxId }
payloadGroups = { 'boxId': boxId, 'comid': comid, 'compvtkey': comkey, 'sid': rjson["result"]["sid"], 'ts': ts, 'key': screctkey }
groupsUnhashed = urlencode(payloadGroups)
groupsSign = hashlib.md5(groupsUnhashed.encode())
headerGroups = { 'boxId': boxId, 'sid': rjson["result"]["sid"], 'comid': comid, 'compvtkey': comkey, 'ts': ts, 'sign': groupsSign.hexdigest() }
commonGroups = { 'common': str(headerGroups) }

rGroups = requests.post(urlGroups, params=groupParams, headers=commonGroups)
configFile = open(fileName, "a")
configFile.write(encrypt(rGroups.text, deviceKey))
configFile.close()
groupJson = rGroups.json()
boxListJson = groupJson["result"]

print("\n[the following groups were detected]")
for group in boxListJson["list"]:
    print("\t", group["groupName"], group["groupId"])
groupId = input("[enter your desired groupid]: ")
pageSize = 5
pageIndex = 1
configParams = { 'boxId': boxId, 'groupId' : groupId, 'pageSize' : pageSize, 'pageIndex' : pageIndex }
payloadConfig = {'boxId' : boxId, 'comid' : comid, 'compvtkey': comkey, 'groupId' : groupId, 'pageIndex' : pageIndex, 'pageSize' : pageSize, 'sid': rjson["result"]["sid"], 'ts': ts, 'key': screctkey}
configUnhashed = urlencode(payloadConfig)
configSign = hashlib.md5(configUnhashed.encode())
headerConfig = { 'boxId': boxId, 'groupId' : groupId, 'pageSize' : pageSize, 'pageIndex' : pageIndex, 'sid': rjson["result"]["sid"], 'comid' : comid, 'compvtkey': comkey, 'ts': ts, 'sign' : configSign.hexdigest()}
commonConfig = { 'common': str(headerConfig) }

rConfig = requests.post(urlConfig, params=configParams, headers=commonConfig)
configFile = open(fileName, "a")
configFile.write(encrypt(rConfig.text, deviceKey))
configFile.close()

jsonCfg = rConfig.json()
realtimeList = jsonCfg["result"]["cfgList"]
print("\n", realtimeList)
