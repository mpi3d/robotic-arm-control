# -*- coding: utf-8 -*-
from time import sleep, time
from Adafruit_PCA9685 import PCA9685

class OneMotor:

    def __init__(self, parameters, position=90, pca9685=PCA9685(), frequency=50):
        self.port = parameters["Port"]
        self.min = round(min(parameters["Min"], parameters["Max"]))
        self.max = round(max(parameters["Min"], parameters["Max"]))
        if "Adjust" in parameters:
            self.adjust = round(parameters["Adjust"])
        else:
            self.adjust = 0
        if "Reverse" in parameters:
            self.reverse = parameters["Reverse"]
        else:
            self.reverse = False
        self.pca9685 = pca9685
        if not frequency is None:
            self.pca9685.set_pwm_freq(frequency)
        self.position = 0
        self.active = True
        self.set(position)
        sleep(0.2)

    def activate(self, activate=True):
        if activate:
            self.active = True
            if self.reverse:
                self.pca9685.set_pwm(self.port, 0, round(((self.max - self.min) / 2 + self.min) * 2)
                                     - self.position + self.adjust)
            else:
                self.pca9685.set_pwm(self.port, 0, self.position + self.adjust)
            sleep(0.2)
        else:
            self.active = False
            self.pca9685.set_pwm(self.port, 0, 0)

    def is_activate(self):
        return self.active

    def set(self, degrees, seconds=0):
        self.active = True
        toff = round((self.max - self.min) / 180 * degrees + self.min)
        toff = min(self.max, toff)
        toff = max(self.min, toff)
        toff = round(toff)
        if self.reverse:
            toff_middle = round(((self.max - self.min) / 2 + self.min) * 2)
        if seconds <= 0:
            interval = 1 / (self.max - self.min) * (max(self.position, toff)
                                                    - min(self.position, toff))
            start = time()
            self.position = toff
            if self.reverse:
                self.pca9685.set_pwm(self.port, 0, toff_middle - self.position + self.adjust)
            else:
                self.pca9685.set_pwm(self.port, 0, self.position + self.adjust)
            sleep(max(interval - time() + start, 0))
        else:
            if toff > self.position:
                interval = seconds / (toff - self.position)
                while toff > self.position:
                    start = time()
                    self.position += 1
                    if self.reverse:
                        self.pca9685.set_pwm(self.port, 0,
                                             toff_middle - self.position + self.adjust)
                    else:
                        self.pca9685.set_pwm(self.port, 0, self.position + self.adjust)
                    sleep(max(interval - time() + start, 0))
            elif toff < self.position:
                interval = seconds / (self.position - toff)
                while toff < self.position:
                    start = time()
                    self.position -= 1
                    if self.reverse:
                        self.pca9685.set_pwm(self.port, 0,
                                             toff_middle - self.position + self.adjust)
                    else:
                        self.pca9685.set_pwm(self.port, 0, self.position + self.adjust)
                    sleep(max(interval - time() + start, 0))
            else:
                start = time()
                self.position = toff
                if self.reverse:
                    self.pca9685.set_pwm(self.port, 0, toff_middle - self.position + self.adjust)
                else:
                    self.pca9685.set_pwm(self.port, 0, self.position + self.adjust)
                sleep(max(seconds - time() + start, 0))

    def get(self):
        return round(180 / (self.max - self.min) * (self.position - self.min))

class TowMotors:

    def __init__(self, parameters, position=90, pca9685=PCA9685(), frequency=50):
        self.left_port = parameters["Left Port"]
        self.right_port = parameters["Right Port"]
        self.min = round(min(parameters["Min"], parameters["Max"]))
        self.max = round(max(parameters["Min"], parameters["Max"]))
        if "Left Adjust" in parameters:
            self.left_adjust = round(parameters["Left Adjust"])
        else:
            self.left_adjust = 0
        if "Right Adjust" in parameters:
            self.right_adjust = round(parameters["Right Adjust"])
        else:
            self.right_adjust = 0
        if "Reverse" in parameters:
            self.reverse = parameters["Reverse"]
        else:
            self.reverse = False
        self.pca9685 = pca9685
        if not frequency is None:
            self.pca9685.set_pwm_freq(frequency)
        self.position = 0
        self.active = True
        self.set(position)
        sleep(0.2)

    def activate(self, activate=True):
        if activate:
            self.active = True
            toff_middle = round(((self.max - self.min) / 2 + self.min) * 2)
            if self.reverse:
                self.pca9685.set_pwm(self.left_port, 0,
                                     toff_middle - self.position + self.left_adjust)
                self.pca9685.set_pwm(self.right_port, 0, self.position + self.right_adjust)
            else:
                self.pca9685.set_pwm(self.left_port, 0, self.position + self.left_adjust)
                self.pca9685.set_pwm(self.right_port, 0,
                                     toff_middle - self.position + self.right_adjust)
            sleep(0.2)
        else:
            self.active = False
            self.pca9685.set_pwm(self.left_port, 0, 0)
            self.pca9685.set_pwm(self.right_port, 0, 0)

    def is_activate(self):
        return self.active

    def set(self, degrees, seconds=0):
        self.active = True
        toff = round((self.max - self.min) / 180 * degrees + self.min)
        toff = min(self.max, toff)
        toff = max(self.min, toff)
        toff_middle = round(((self.max - self.min) / 2 + self.min) * 2)
        if seconds <= 0:
            interval = 1 / (self.max - self.min) * (max(self.position, toff)
                                                    - min(self.position, toff))
            start = time()
            self.position = toff
            if self.reverse:
                self.pca9685.set_pwm(self.left_port, 0,
                                     toff_middle - self.position + self.left_adjust)
                self.pca9685.set_pwm(self.right_port, 0, self.position + self.right_adjust)
            else:
                self.pca9685.set_pwm(self.left_port, 0, self.position + self.left_adjust)
                self.pca9685.set_pwm(self.right_port, 0,
                                     toff_middle - self.position + self.right_adjust)
            sleep(max(interval - time() + start, 0))
        else:
            if toff > self.position:
                interval = seconds / (toff - self.position)
                while toff > self.position:
                    start = time()
                    self.position += 1
                    if self.reverse:
                        self.pca9685.set_pwm(self.left_port, 0,
                                             toff_middle - self.position + self.left_adjust)
                        self.pca9685.set_pwm(self.right_port, 0, self.position + self.right_adjust)
                    else:
                        self.pca9685.set_pwm(self.left_port, 0, self.position + self.left_adjust)
                        self.pca9685.set_pwm(self.right_port, 0,
                                             toff_middle - self.position + self.right_adjust)
                    sleep(max(interval - time() + start, 0))
            elif toff < self.position:
                interval = seconds / (self.position - toff)
                while toff < self.position:
                    start = time()
                    self.position -= 1
                    if self.reverse:
                        self.pca9685.set_pwm(self.left_port, 0,
                                             toff_middle - self.position + self.left_adjust)
                        self.pca9685.set_pwm(self.right_port, 0, self.position + self.right_adjust)
                    else:
                        self.pca9685.set_pwm(self.left_port, 0, self.position + self.left_adjust)
                        self.pca9685.set_pwm(self.right_port, 0,
                                             toff_middle - self.position + self.right_adjust)
                    sleep(max(interval - time() + start, 0))
            else:
                start = time()
                self.position = toff
                if self.reverse:
                    self.pca9685.set_pwm(self.left_port, 0,
                                         toff_middle - self.position + self.left_adjust)
                    self.pca9685.set_pwm(self.right_port, 0, self.position + self.right_adjust)
                else:
                    self.pca9685.set_pwm(self.left_port, 0, self.position + self.left_adjust)
                    self.pca9685.set_pwm(self.right_port, 0,
                                         toff_middle - self.position + self.right_adjust)
                sleep(max(seconds - time() + start, 0))

    def get(self):
        return round(180 / (self.max - self.min) * (self.position - self.min))

class Arm:

    def __init__(self, parameters, positions=(90, 90, 90, 90, 90), pca9685=PCA9685(), frequency=50):
        self.pca9685 = pca9685
        if not frequency is None:
            self.pca9685.set_pwm_freq(frequency)
        self.base = OneMotor(parameters[0], positions[0], self.pca9685, None)
        self.shoulder = TowMotors(parameters[1], positions[1], self.pca9685, None)
        self.elbow = OneMotor(parameters[2], positions[2], self.pca9685, None)
        self.wrist = OneMotor(parameters[3], positions[3], self.pca9685, None)
        self.wrench = OneMotor(parameters[4], positions[4], self.pca9685, None)

    def activate(self, activate=True):
        self.base.activate(activate)
        self.shoulder.activate(activate)
        self.elbow.activate(activate)
        self.wrist.activate(activate)
        self.wrench.activate(activate)

    def is_activate(self):
        return self.base.is_activate() \
               and self.shoulder.is_activate() \
               and self.elbow.is_activate() \
               and self.wrist.is_activate() \
               and self.wrench.is_activate()

    def set(self, degrees, seconds=0):
        seconds = seconds / 5
        self.base.set(degrees[0], seconds)
        self.shoulder.set(degrees[1], seconds)
        self.elbow.set(degrees[2], seconds)
        self.wrist.set(degrees[3], seconds)
        self.wrench.set(degrees[4], seconds)

    def get(self):
        return (self.base.get(),
                self.shoulder.get(),
                self.elbow.get(),
                self.wrist.get(),
                self.wrench.get())
