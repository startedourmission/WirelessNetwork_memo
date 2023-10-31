from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus,unquote
import requests

import serial

url = 'https://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty'
queryParams = '?' + urlencode({
quote_plus('serviceKey') : 'lZGidnu18HbWbm2BKikXefvoJCRe3GAMMJAXneSYYseXYTZOe2xFmAbCQkVlxu1SfgSiItxBxv+RaMaSWG1wvQ=='
	,quote_plus('returnType') : 'xml'
	,quote_plus('numOfRows') : '10'
	,quote_plus('pageNo') : '1'
	,quote_plus('stationName') : '주안'
	,quote_plus('dataTerm') : 'DAILY'
	,quote_plus('ver') : '1.0'})


res = requests.get(url + queryParams)
soup = BeautifulSoup(res.content,'html.parser')
data = soup.find_all('item')
#print(data)

parse_datatime = 0
parse_dust = 0
for item in data:
    datatime = item.find("datatime")
    pm25value = item.find("pm25value")
    parse_datatime = datatime.get_text()
    parse_dust = float(pm25value.get_text())
    print(parse_datatime)
    print(parse_dust)
    break

port = '/dev/ttyACM0'
brate = 9600
pybrate = 57600

seri = serial.Serial(port, baudrate = brate, timeout = None)
print(seri.name)
seri.write(b'\x0101')

import pyfirmata
import time
board = pyfirmata.Arduino(port)
board.digital[7].mode = pyfirmata.OUTPUT

a = 1
cont = 0.0
ard_dust = 0

while True:
    if seri.in_waiting !=0:
	    content = seri.readline()
	    ard_dust = float(content.decode())
	    print(ard_dust)

    if ard_dust > parse_dust:
        print("open window")
        board.digital[7].write(1)
    elif ard_dust < parse_dust:
        print("close window")
        board.digital[7].write(0)
    time.sleep(1)

