from Crypto.Cipher import DES3   
from Crypto.Util.Padding import pad, unpad
import base64, hashlib, os, re, uuid, platform, subprocess, sys, fcntl, struct, pathlib, getpass

deviceKey = "ourHardworkByTheseWordsGuardedPleaseDontSteal(C)DICOT"
fileName = uuid.uuid3(uuid.NAMESPACE_DNS, getpass.getuser())

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
        return '-'.join(hddsn)
    return print('[unsupported platform!]')

print("[welcome to dicli licensor! initiating license process...]\n")

licenseFile = open("%s.dat" % fileName, "w")
licenseFile.write(encrypt("---start of license---\n", deviceKey))
licenseFile.close()

licenseFile = open("%s.dat" % fileName, "a")
print('MAC:    ', end="")
print(':'.join(re.findall('..', '%012x' % uuid.getnode())))
pMAC = ''.join(re.findall('..', '%012x' % uuid.getnode()))
licenseFile.write(encrypt(pMAC + '$', deviceKey))
licenseFile.close()

licenseFile = open("%s.dat" % fileName, "a")
print('UUID:   ', end="")
print(cpu_info())
licenseFile.write(encrypt(cpu_info() + '$', deviceKey))
licenseFile.close()

licenseFile = open("%s.dat" % fileName, "a")
print('HDD SN: ', end="")
print(disk_id())
licenseFile.write(encrypt(disk_id(), deviceKey))
licenseFile.close()

licenseFile = open("%s.dat" % fileName, "a")
licenseFile.write(encrypt("\n---end of license---\n\n", deviceKey))
licenseFile.close()
print("\n[successfully generated license file]\n")
