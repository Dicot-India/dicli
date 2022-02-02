import requests
import hashlib
import time
import json
import sys
from urllib.parse import urlencode

print("Welcome to DIcot CLI! Initiating login process...\n")

alias = input("Alias: ")
pUnhashed = input("Password: ")
pHashed = hashlib.md5(pUnhashed.encode())
comid = "100"
comkey = "8919244ff15d441bae4b944b112a33ea"
screctkey = "f1cd9351930d4e589922edbcf3b09a7c"
ts = str(int(time.time()))

def loginError():
    print("Error while logging in! Exitting...\n")
    sys.exit(1)

urlEU = "http://api.eu.v-box.net/box-data/api/we-data/login"
urlBoxs = "http://api.eu.v-box.net/box-data/api/we-data/boxs"
urlParams = { 'alias': alias, 'password': pHashed.hexdigest() }
payload = { 'alias': alias, 'comid': comid, 'compvtkey': comkey, 'password': pHashed.hexdigest(), 'ts': ts, 'key': screctkey }
signUnhashed = urlencode(payload)
signHashed = hashlib.md5(signUnhashed.encode())
common = { 'compvtkey': comkey, 'sign': signHashed.hexdigest(), 'comid': comid, 'ts': ts }
commonHeader = {'common': str(common)}

print("\nAttempting login...\n")
r = requests.post(urlEU, params=urlParams, headers=commonHeader)
if(r.status_code == 200):
    print("Succesfully logged in! Fetching boxes list...\n")
else:
    loginError()
rjson = r.json()
payloadBoxs = { 'comid': comid, 'compvtkey': comkey, 'sid': rjson["result"]["sid"], 'ts': ts, 'key': screctkey }
boxsUnhashed = urlencode(payloadBoxs)
boxsSign = hashlib.md5(boxsUnhashed.encode())
headerBoxs = { 'sid': rjson["result"]["sid"], 'comid': comid, 'compvtkey': comkey, 'ts': ts, 'sign': boxsSign.hexdigest() }
commonBoxs = { 'common': str(headerBoxs) }

rBoxs = requests.post(urlBoxs, headers=commonBoxs)
print(rBoxs.text)
boxsJson = rBoxs.json()
initialBox = str(boxsJson["result"]["list"])
listStr = initialBox[initialBox.find("[")+1:initialBox.rfind("]")]
listJson = listStr[listStr.find("[")+1:listStr.rfind("]")]
boxFinal = listJson[listJson.find("boxId")+8:listJson.rfind("}")]
print(boxFinal)
