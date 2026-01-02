import odroid_wiringpi as wpi
import time


FAN_PIN = 7
CLK = 19
RNG = 1024

# wiringPi 초기화
wpi.wiringPiSetup()

# 하드웨어 PWM 설정
wpi.pinMode(FAN_PIN, wpi.PWM_OUTPUT)
wpi.pwmSetClock(CLK)    # 25kHz 주파수 (19.2MHz / 19 / 1024 ≈ 25kHz)
wpi.pwmSetRange(RNG)  # 0-1024 범위

def fan_on():
    duty_value = int(RNG)
    wpi.pwmWrite(FAN_PIN, duty_value)

def fan_off():
    wpi.pwmWrite(FAN_PIN, 0)

try:
    fan_off()
    time.sleep(1)

    while True:
        fan_on()
        time.sleep(5)
        fan_off()
        time.sleep(1)

except KeyboardInterrupt:
    print("\n프로그램 종료")

finally:
    fan_off()
