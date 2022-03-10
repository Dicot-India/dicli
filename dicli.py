from tokenize import group
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
urlGroups = "http://api.eu.v-box.net/box-data/api/we-data/realgroups"
urlConfig = "http://api.eu.v-box.net/box-data/api/we-data/realcfgs"
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
#boxId = listJson[listJson.find("boxId")+8:listJson.rfind("}")]
boxId = input("Enter your desired boxId: ")
groupParams = { 'boxId': boxId }
payloadGroups = { 'boxId': boxId, 'comid': comid, 'compvtkey': comkey, 'sid': rjson["result"]["sid"], 'ts': ts, 'key': screctkey }
groupsUnhashed = urlencode(payloadGroups)
groupsSign = hashlib.md5(groupsUnhashed.encode())
headerGroups = { 'boxId': boxId, 'sid': rjson["result"]["sid"], 'comid': comid, 'compvtkey': comkey, 'ts': ts, 'sign': groupsSign.hexdigest() }
commonGroups = { 'common': str(headerGroups) }

rGroups = requests.post(urlGroups, params=groupParams, headers=commonGroups)
print(rGroups.text)
groupJson = rGroups.json()
initialGroup = str(groupJson["result"]["list"])
groupStr = initialGroup[initialGroup.find("[")+1:initialGroup.rfind("]")]
#groupId = groupStr[groupStr.find("groupId")+10:groupStr.find("}")]
print("The groups list is as follows:")
boxList = str(groupJson["result"])
boxListJson = groupJson["result"]
print(boxList)
print("The type of object is ", type(boxList))

for group in boxListJson["list"]:
    print(group["groupName"], group["groupId"])
groupId = input("Enter desired groupId: ")
pageSize = 5
pageIndex = 2
configParams = { 'boxId': boxId, 'groupId' : groupId, 'pageSize' : pageSize, 'pageIndex' : pageIndex }
payloadConfig = {'boxId' : boxId, 'comid' : comid, 'compvtkey': comkey, 'groupId' : groupId, 'pageIndex' : pageIndex, 'pageSize' : pageSize, 'sid': rjson["result"]["sid"], 'ts': ts, 'key': screctkey}
configUnhashed = urlencode(payloadConfig)
configSign = hashlib.md5(configUnhashed.encode())
headerConfig = { 'boxId': boxId, 'groupId' : groupId, 'pageSize' : pageSize, 'pageIndex' : pageIndex, 'sid': rjson["result"]["sid"], 'comid' : comid, 'compvtkey': comkey, 'ts': ts, 'sign' : configSign.hexdigest()}
commonConfig = { 'common': str(headerConfig) }

rConfig = requests.post(urlConfig, params=configParams, headers=commonConfig)
print(rConfig.text)

