# INHATC_2023_2_WirelessNetwork

인하공업전문대학 2023년도 2학기 무선네트워크

> 2023.09.26
> 추석 연휴 강의는 녹화강의로 대체, 과제 없거나 간단하게 있음.  
> 2023.10.10
> 중간 실습 평가 다 봄. influxdb까지만 하고 grafana 시각화는 안함.

## 라즈베리파이

#### 초기 설정

- sd 카드 포맷 & 라즈비언 OS 이미지파일 다운로드

- 라즈베리 파이에 sd카드, 전원, 입출력장치 및 랜선 연결

- 부팅 후 언어 설정. 네트워크 설정은 건너뜀

- apt update & upgrade

```bash
sudo apt update
sudo apt upgrade
```

* 한글 깨짐

```bash
sudo apt-get install fonts-unfonts-core -y
sudo apt-get install ibus ibus-hangul -y
sudo reboot
```

- 네트워크 설정
```Shell
sudo vim /etc/dhcpcd.conf
```

#### InfluxDB2 

- InfluxDB download key using wget

```
wget -q https://repos.influxdata.com/influxdata-archive_compat.key

echo '393e8779c89ac8d958f81f942f9ad7fb82a25e133faddaf92e15b16e6ac9ce4c influxdata-archive_compat.key' | sha256sum -c && cat influxdata-archive_compat.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg > /dev/null

echo 'deb [signed-by=/etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg] https://repos.influxdata.com/debian stable main' | sudo tee /etc/apt/sources.list.d/influxdata.list
```
	위 작업을 안하면 apt로 설치를 해도 정상적인 실행이 안됨.


- Packages are up to date && install Influxdb2

```
sudo apt-get update && sudo apt-get install influxdb2 -y
```

- error) influxdb2 패키지 찾을수 없습니다.
    - influxdb 1으로 설치

```
sudo apt-get install influxdb -y
```

- InfluxDB as a background service on startup

```
sudo service influxdb start
```

- InfluxDB is status (service)

```
sudo service influxdb status
```

- InfluxDB Python Library

```Shell
sudo pip3 install influxdb
```
### InfluxDB2 web setting

- localhost:8086 접속
- GET STARTED

[![](https://raw.githubusercontent.com/sonnonet/2023_inhatc/main/capture/influxdb_1.png)](https://github.com/sonnonet/2023_inhatc/blob/main/capture/influxdb_1.png)

- Setup Initial User
- (pi , raspberry)
- Organization Name (study)
- Bucket Name (DatabaseName)
    - test

[![](https://raw.githubusercontent.com/sonnonet/2023_inhatc/main/capture/influxdb_2.png)](https://github.com/sonnonet/2023_inhatc/blob/main/capture/influxdb_2.png)

### Grafana Installation

1. Repository의 GPG key를 더하기

```
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
```

2. Repository를 더하기

```
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
```

3. 프로그램 설치

```
sudo apt update
sudo apt install grafana
```

4. 프로그램 실행

```
sudo service grafana-server start
```

localhot 또는 라즈베리파이의 ip :3000

## 아두이노 기기 & 센서

아두이노 센서는 주로 3.3V or 5V 사용한다. 5V 센서는 3.3V에 꽂아도 되지만 그 반대는 센서가 탈 수 있음
아두이노 기준으로, 디지털 신호는 송수신 모두 가능하지만, 아날로그 신호는 수신만 가능

#### 인체감지센서 

Python 코드 :  pir.py

#### 미세먼지 센서 

센서에 있는 구멍을 이용해 미세먼지 투과율을 측정 , 적외선 LED 작동
미세먼지 수치를 아날로그 데이터 전압(0 ~ 1023)값으로 표현

> Voltage = 아날로그 핀 값 x 5.0 / 1023.0  
> dustDestiny = (Voltage - 0.3) / 0.005

- VCC - 5V
- 아두이노의 디지털 핀에  LED 입력
- 센서의 out - 아두이노 A0

#### 카메라

- 기본 설정
```Shell
sudo raspi-config
```

Interface Option > Legacy Camera enable 선택

- Legacy Camera enable

```Shell
raspistill -o 파일명.jpg -t 1000 # 1초 뒤 촬영
raspistill -o 파일명.jpg -vf -vh # 수평, 수직 반전 
```

- Legacy Camera disable

```Shell
libcamera-still -o 파일명.jpg
```



- 텔레그램 챗봇으로 전송

![[Pasted image 20230926154859.png]]
job.context > job.chat_id로 변경
async / await 사용

- Picamera2 로 변경

```Python
from picamera2 import Picamera2, Preview

picam = Picamera2()

config = picam.create_preview_configuration()
picam.confihure(config)

picam.start_preview(Preview.QTGL)

picam.start()
time.sleep(2)
picam.capture_file(“image.jpg”)

picam.close()

```






