from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad
from pathlib import Path
import hashlib
import base64
import os

deviceKey = "ourHardworkByTheseWordsGuardedPleaseDontSteal(C)DICOT"

def hashKey(key):
    return hashlib.md5(bytes(key, encoding='utf8'))

def decrypt(message, unhashedKey):
    key = hashKey(unhashedKey)
    decipher = DES3.new(key.digest(), DES3.MODE_ECB)
    decipheredText = decipher.decrypt(base64.b64decode(message.encode('utf8')))
    decryptedText = unpad(decipheredText, 8, style='pkcs7').decode('UTF8')
    return decryptedText

path_to_file = 'dicli.conf'
path = Path(path_to_file)

print("[welcome to dicli config reader!]\n")
if path.is_file():
    print("[reading dicli.conf]\n")
    fp = open("dicli.conf", "r")
    print(decrypt(fp.read(), deviceKey))
else:
    print('\033[91m' + '[dicli.conf not found!]\n' + '\033[0m')
