#!/usr/bin/env python3
"""
Odroid M1S Fan Controller (fanboy)
- 부팅 후 5초간 팬 작동
- CPU 온도 50°C 초과 시 팬 ON, 이하 시 팬 OFF
"""

import odroid_wiringpi as wpi
import time
import signal
import sys
import os

# PWM 설정
FAN_PIN = 7 # HW PWM 2
CLK = 19
RNG = 1024


TEMP_THRESHOLD = 50000  # 50°C 
TEMP_FILE = "/sys/devices/virtual/thermal/thermal_zone0/temp"

CHECK_INTERVAL = 5

LOG_INTERVAL = 60

# 부팅 시 팬 작동 시간
BOOT_FAN_DURATION = 5


def main():
    fan_running = False
    last_log_time = 0
    
    def cleanup(signum=None, frame=None):
        nonlocal fan_running
        wpi.pwmWrite(FAN_PIN, 0)
        fan_running = False
        temp_fd.close()
        sys.exit(0)

    signal.signal(signal.SIGTERM, cleanup)
    signal.signal(signal.SIGINT, cleanup)

    wpi.wiringPiSetup()
    wpi.pinMode(FAN_PIN, wpi.PWM_OUTPUT)
    wpi.pwmSetClock(CLK)
    wpi.pwmSetRange(RNG)

    temp_fd = os.open(TEMP_FILE, os.O_RDONLY)

    wpi.pwmWrite(FAN_PIN, RNG)
    fan_running = True
    time.sleep(BOOT_FAN_DURATION)
    wpi.pwmWrite(FAN_PIN, 0)
    fan_running = False

    last_log_time = time.time()

    while True:
        # 온도 읽기 (seek + read, 파일 재오픈 없이)
        os.lseek(temp_fd, 0, os.SEEK_SET)
        temp = int(os.read(temp_fd, 16).strip())

        if temp > TEMP_THRESHOLD:
            if not fan_running:
                wpi.pwmWrite(FAN_PIN, RNG)
                fan_running = True
        else:
            if fan_running:
                wpi.pwmWrite(FAN_PIN, 0)
                fan_running = False

        # log 1분 간격
        now = time.time()
        if now - last_log_time >= LOG_INTERVAL:
            print(f"[STATUS] {temp // 1000}C / FAN: {'ON' if fan_running else 'OFF'}", flush=True)
            last_log_time = now

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
