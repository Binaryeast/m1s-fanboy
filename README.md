# Fanboy - Odroid M1S Fan Control Controller

## 기능
- 부팅 직후 5초간 팬 작동 (작동 테스트)
- CPU 온도 50°C 초과 시 팬 ON
- CPU 온도 50°C 이하 시 팬 OFF
- 5초 간격 온도 체크, 1분 간격 로그

## TODO

- [ ] deb for apt
- [ ] ppa
  

## 설치

### requirements

```bash
sudo apt install python3 python3-pip odroid-wiringpi -y
sudo pip3 install odroid-wiringpi
```

python global package install?

### Install

```bash
sudo cp fanboy.py /opt/fanboy.py
sudo chmod +x /opt/fanboy.py
sudo cp fanboy.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable fanboy.service
sudo systemctl start fanboy.service
```


## 서비스 관리

### 로그 확인

```bash
sudo systemctl status fanboy.service
journalctl -u fanboy.service -f    # 실시간 로그
journalctl -u fan-control.service -n 50    # 최근 50줄
```

### 서비스 관리

```bash
sudo systemctl start fanboy.service    # 시작
sudo systemctl stop fanboy.service     # 중지
sudo systemctl restart fanboy.service  # 재시작
sudo systemctl disable fanboy.service  # 자동시작 해제
```
