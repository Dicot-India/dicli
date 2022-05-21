md C:\dicli
echo F|xcopy %~dp0\dicli.py C:\dicli\_dicli.py
echo py _dicli.py>C:\dicli\dicli.bat
setx /M path "%path%;C:\dicli"
refreshenv
