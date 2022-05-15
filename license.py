from Crypto.Cipher import DES3   
from Crypto.Util.Padding import pad, unpad
import base64, hashlib, os, re, uuid, platform

deviceKey = "ourHardworkByTheseWordsGuardedPleaseDontSteal(C)DICOT"

def hashKey(key):
    return hashlib.md5(bytes(key, encoding='utf8'))

def encrypt(message, unhashedKey):
    key = hashKey(unhashedKey)
    cipher = DES3.new(key.digest(), DES3.MODE_ECB)
    cipherText = cipher.encrypt(pad(message.encode('UTF8'), 8, style='pkcs7'))
    encryptedText = base64.b64encode(cipherText).decode('utf8')
    return encryptedText

def cpu_info():
    if platform.system() == 'Linux':
        command = 'cat /proc/cpuinfo'
        return os.popen(command).read().strip()
    elif platform.system() == 'Windows':
        return platform.processor()
    return print('[unsupported platform!]')

print("[welcome to dicli licensor! initiating license process...]\n")

print('MAC: ', end="")
print(':'.join(re.findall('..', '%012x' % uuid.getnode())))
print(cpu_info())

# configFile = open(fileName, "w")
# r = requests.post(urlEU, params=urlParams, headers=commonHeader)
# if(r.status_code == 200):
#     configFile.write(encrypt(r.text, deviceKey))
#     configFile.close()
#     print("[succesfully logged in! fetching boxes list...]\n")
# else:
#     configFile.close()
#     loginError()
#
# configFile = open(fileName, "a")
# configFile.write(encrypt(rConfig.text, deviceKey))
# configFile.close()
