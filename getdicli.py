import ctypes, platform, os, sys, subprocess

def isAdmin():
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin

def dicliLinux():
    print('\n[setting up for linux]')
    print('[checking permissions]')
    if os.geteuid() > 0:
        print('[permission denied! must be root]\n')
        sys.exit(1)

    subprocess.call(['bash', './dicli/lin.sh'])

    print('[end of install - you may invoke the program by typing ' + '\033[1m' + 'dicli' + '\033[0m' + ' at the command line]')

def dicliWindows():
    print('\n[setting up for windows]')
    print('[checking permissions]')
    if isAdmin():
        subprocess.call([r'dicli\win.bat'])
        print('\n[installation successful! after refreshing environment variables, run dicli at the command line to invoke the program]')
    else:
        print('[permission denied! must be admin]\n')
        sys.exit(1)


print('[welcome to dicli installer! initiating install procedure]\n')

print('[fetching installation files]\n')
os.system("git clone https://github.com/dicot-india/dicli")

if platform.system()  == 'Linux':
    dicliLinux()
elif platform.system() == 'Windows':
    dicliWindows()
else:
    print('\033[91m' + '[unsupported platform!]' + '\033[0m')

