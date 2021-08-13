import RPi.GPIO as gpio
import time

R1 = 23 #forward
R2 = 24 #reverse
R3 = 6 #enable
L1 = 17
L2 = 27
L3 = 5
L_MULT = 1.405
pins = [R1, R2, R3, L1, L2, L3]

class robot():
    def __init__(self):
        gpio.setwarnings(False)
        gpio.setmode(gpio.BCM)
        for i in pins:
            gpio.setup(i, gpio.OUT)
            gpio.output(i, gpio.LOW)
        self.LPWM = gpio.PWM(L3, 100)
        self.RPWM = gpio.PWM(R3, 100)

    def __del__(self):
        gpio.cleanup()

    def forward(self, runtime, speed):
        gpio.output(L1, True)
        gpio.output(L2, False)
        gpio.output(R1, False)
        gpio.output(R2, True)
        self.LPWM.start(speed*L_MULT)
        self.RPWM.start(speed)
        time.sleep(runtime)
        self.stop()

    def reverse(self, runtime, speed):
        gpio.output(L1, False)
        gpio.output(L2, True)
        gpio.output(R1, True)
        gpio.output(R2, False)
        self.LPWM.start(speed*L_MULT)
        self.RPWM.start(speed)
        time.sleep(runtime)
        self.stop()
    
    def left(self, runtime):
        gpio.output(L1, False)
        gpio.output(L2, True)
        gpio.output(R1, False)
        gpio.output(R2, True)
        self.LPWM.start(30*L_MULT)
        self.RPWM.start(30)
        time.sleep(runtime)
        self.stop()
    
    def right(self, runtime):
        gpio.output(L1, True)
        gpio.output(L2, False)
        gpio.output(R1, True)
        gpio.output(R2, False)
        self.LPWM.start(30*L_MULT)
        self.RPWM.start(30)
        time.sleep(runtime)
        self.stop()
    
    def stop(self):
        gpio.output(L1, False)
        gpio.output(L2, False)
        gpio.output(R1, False)
        gpio.output(R2, False)
