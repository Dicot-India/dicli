import platform, os

def dicliLinux():
    print('\n[running on linux]\n')
    print('[end of install - you may invoke the program by typing ' + '\033[1m' + 'dicli' + '\033[0m' + ' at the command line]')

def dicliWindows():
    print('\n[running on windows]\n')

print('[welcome to dicli installer! initiating install procedure]\n')
if platform.system()  == 'Linux':
    dicliLinux()
elif platform.system() == 'Windows':
    dicliWindows()
else:
    print('\033[91m' + '[unsupported platform!]' + '\033[0m')

