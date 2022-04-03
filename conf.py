from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad
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

print("[reading dicli.conf]\n")
fp = open("dicli.conf", "r")
print(decrypt(fp.read(), deviceKey))
