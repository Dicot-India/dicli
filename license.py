from Crypto.Cipher import DES3   
from Crypto.Util.Padding import pad, unpad
import base64, hashlib, os, re, uuid, platform, subprocess, sys, fcntl, struct, pathlib

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
        command = 'cat /etc/machine-id'
        return os.popen(command).read().strip()
    elif platform.system() == 'Windows':
        return subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
    return print('[unsupported platform!]')

def disk_id():
    if platform.system() == 'Linux':
        if os.geteuid() > 0:
            print('[permission denied! must be root]')
            sys.exit(1)
        command = "df -P /etc/machine-id | tail -1 | cut -d' ' -f 1"
        driveId = os.popen(command).read().strip()
        with open(driveId, "rb") as fd:
            hd_driveid_format_str = "@ 10H 20s 3H 8s 40s 2B H 2B H 4B 6H 2B I 36H I Q 152H"
            HDIO_GET_IDENTITY = 0x030d
            sizeof_hd_driveid = struct.calcsize(hd_driveid_format_str)
            assert sizeof_hd_driveid == 512
            buf = fcntl.ioctl(fd, HDIO_GET_IDENTITY, " " * sizeof_hd_driveid)
            fields = struct.unpack(hd_driveid_format_str, buf)
            serial_no = fields[10].strip()
        return serial_no.decode("utf-8")
    elif platform.system() == 'Windows':
        hddsn = subprocess.check_output('wmic diskdrive get SerialNumber').decode().split('\n')[1:]
        hddsn = [s.strip() for s in hddsn if s.strip()]
        return print('-'.join(hddsn))
    return print('[unsupported platform!]')

print("[welcome to dicli licensor! initiating license process...]\n")

print('MAC:    ', end="")
print(':'.join(re.findall('..', '%012x' % uuid.getnode())))
print('UUID:   ', end="")
print(cpu_info())
print('HDD SN: ', end="")
print(disk_id())

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
