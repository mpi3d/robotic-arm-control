# -*- coding: utf-8 -*-

"""
Module to control the Robotic Arm: https://github.com/MPi3D/Robotic_Arm.
"""

from time import sleep, time
from Adafruit_PCA9685 import PCA9685

class OneMotor:

    """
    Class to control an articulation which has only one motor.

    Arguments:
        parameters (dict): The dictionary with the articulation parameters:
            "port" (int): The port number of the articulation.
            "min" (int): The minimum toff for the articulation.
            "max" (int): The maximum toff for the articulation.
            "adjust" (int): The value in toff to adjust the motor of the articulation.
                            Default is 0.
            "reverse" (bool): The boolean which specifies if the direction should be inverted.
                              Default is False.
        position (int): The position to start in degrees. Default is 90.
        pca9685 (object): The PCA9685 object. Default is PCA9685().
        frequency (int): The frequency to be set. None for non set. Default is 50.

    Attributes:
        port (int): The port number from parameters["port"] argument.
        min (int): The minimum toff from parameters["min"] argument.
        max (int): The maximum toff from parameters["max"] argument.
        adjust (int): The adjust value in toff from parameters["adjust"] argument.
        reverse (bool): The reverse boolean from parameters["reverse"] argument.
        position (int): The current position in toff of the articulation.
        pca9685 (object): The PCA9685 object from pca9685 argument.
        active (bool): The boolean which specifies if the articulation is active or not.
    """

    def __init__(self, parameters, position=90, pca9685=PCA9685(), frequency=50):

        self.port = parameters["port"]
        self.min = round(min(parameters["min"], parameters["max"]))
        self.max = round(max(parameters["min"], parameters["max"]))
        if "adjust" in parameters:
            self.adjust = round(parameters["adjust"])
        else:
            self.adjust = 0
        if "reverse" in parameters:
            self.reverse = parameters["reverse"]
        else:
            self.reverse = False
        self.pca9685 = pca9685
        if not frequency is None:
            self.pca9685.set_pwm_freq(frequency)
        self.position = 0
        self.active = True
        self.set_position(position)
        sleep(0.2)

    def set_active(self, active=True):

        """
        Function to active or deactive the articulation.

        Arguments:
            active (bool): The boolean to activate or deactivate the articulation. Default is True.
        """

        if active:
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

    def is_active(self):

        """
        Function to get the status active or deactive of the articulation.

        Returns:
            active (bool): The boolean which specifies if the articulation is active or deactive.
        """

        return self.active

    def set_position(self, degrees, seconds=0):

        """
        Function to set the position of the articulation.

        Arguments:
            degrees (int): The degrees to set the position.
            seconds (float): The time in seconds to go to the position. Default is 0.
        """

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

    def get_position(self):

        """
        Function to get the position of the articulation.

        Returns:
            degrees (int): The degrees of the position.
        """

        return round(180 / (self.max - self.min) * (self.position - self.min))

class TwoMotors:

    """
    Class to control an articulation with two motors.

    Arguments:
        parameters (dict): The dictionary with the articulation parameters:
            "right port" (int): The right port number of the articulation.
            "left port" (int): The left port number of the articulation.
            "min" (int): The minimum toff for the articulation.
            "max" (int): The maximum toff for the articulation.
            "right adjust" (int): The value in toff to adjust the right motor of the articulation.
                                  Default is 0.
            "left adjust" (int): The value in toff to adjust the left motor of the articulation.
                                 Default is 0.
            "reverse" (bool): The boolean which specifies if the direction should be inverted.
                              Default is False.
        position (int): The position to start in degrees. Default is 90.
        pca9685 (object): The PCA9685 object. Default is PCA9685().
        frequency (int): The frequency to be set. None for non set. Default is 50.

    Attributes:
        right_port (int): The right port number from parameters["right port"] argument.
        left_port (int): The left port number from parameters["left port"] argument.
        min (int): The minimum toff from parameters["min"] argument.
        max (int): The maximum toff from parameters["max"] argument.
        right_adjust (int): The right adjust value in toff from parameters["right adjust"] argument.
        left_adjust (int): The left adjust value in toff from parameters["left adjust"] argument.
        reverse (bool): The reverse boolean from parameters["reverse"] argument.
        position (int): The current position in toff of the articulation.
        pca9685 (object): The PCA9685 object from pca9685 argument.
        active (bool): The boolean which specifies if the articulation is active or not.
    """

    def __init__(self, parameters, position=90, pca9685=PCA9685(), frequency=50):
        self.right_port = parameters["right port"]
        self.left_port = parameters["left port"]
        self.min = round(min(parameters["min"], parameters["max"]))
        self.max = round(max(parameters["min"], parameters["max"]))
        if "right adjust" in parameters:
            self.right_adjust = round(parameters["right adjust"])
        else:
            self.right_adjust = 0
        if "left adjust" in parameters:
            self.left_adjust = round(parameters["left adjust"])
        else:
            self.left_adjust = 0
        if "reverse" in parameters:
            self.reverse = parameters["reverse"]
        else:
            self.reverse = False
        self.pca9685 = pca9685
        if not frequency is None:
            self.pca9685.set_pwm_freq(frequency)
        self.position = 0
        self.active = True
        self.set_position(position)
        sleep(0.2)

    def set_active(self, active=True):

        """
        Function to active or deactive the articulation.

        Arguments:
            active (bool): The boolean to activate or deactivate the articulation. Default is True.
        """

        if active:
            self.active = True
            toff_middle = round(((self.max - self.min) / 2 + self.min) * 2)
            if self.reverse:
                self.pca9685.set_pwm(self.right_port, 0,
                                     toff_middle - self.position + self.right_adjust)
                self.pca9685.set_pwm(self.left_port, 0, self.position + self.left_adjust)
            else:
                self.pca9685.set_pwm(self.right_port, 0, self.position + self.right_adjust)
                self.pca9685.set_pwm(self.left_port, 0,
                                     toff_middle - self.position + self.left_adjust)
            sleep(0.2)
        else:
            self.active = False
            self.pca9685.set_pwm(self.right_port, 0, 0)
            self.pca9685.set_pwm(self.left_port, 0, 0)

    def is_active(self):

        """
        Function to get the status active or deactive of the articulation.

        Returns:
            active (bool): The boolean which specifies if the articulation is active or deactive.
        """

        return self.active

    def set_position(self, degrees, seconds=0):

        """
        Function to set the position of the articulation.

        Arguments:
            degrees (int): The degrees to set the position.
            seconds (float): The time in seconds to go to the position. Default is 0.
        """

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
                self.pca9685.set_pwm(self.right_port, 0,
                                     toff_middle - self.position + self.right_adjust)
                self.pca9685.set_pwm(self.left_port, 0, self.position + self.left_adjust)
            else:
                self.pca9685.set_pwm(self.right_port, 0, self.position + self.right_adjust)
                self.pca9685.set_pwm(self.left_port, 0,
                                     toff_middle - self.position + self.left_adjust)
            sleep(max(interval - time() + start, 0))
        else:
            if toff > self.position:
                interval = seconds / (toff - self.position)
                while toff > self.position:
                    start = time()
                    self.position += 1
                    if self.reverse:
                        self.pca9685.set_pwm(self.right_port, 0,
                                             toff_middle - self.position + self.right_adjust)
                        self.pca9685.set_pwm(self.left_port, 0, self.position + self.left_adjust)
                    else:
                        self.pca9685.set_pwm(self.right_port, 0, self.position + self.right_adjust)
                        self.pca9685.set_pwm(self.left_port, 0,
                                             toff_middle - self.position + self.left_adjust)
                    sleep(max(interval - time() + start, 0))
            elif toff < self.position:
                interval = seconds / (self.position - toff)
                while toff < self.position:
                    start = time()
                    self.position -= 1
                    if self.reverse:
                        self.pca9685.set_pwm(self.right_port, 0,
                                             toff_middle - self.position + self.right_adjust)
                        self.pca9685.set_pwm(self.left_port, 0, self.position + self.left_adjust)
                    else:
                        self.pca9685.set_pwm(self.right_port, 0, self.position + self.right_adjust)
                        self.pca9685.set_pwm(self.left_port, 0,
                                             toff_middle - self.position + self.left_adjust)
                    sleep(max(interval - time() + start, 0))
            else:
                start = time()
                self.position = toff
                if self.reverse:
                    self.pca9685.set_pwm(self.right_port, 0,
                                         toff_middle - self.position + self.right_adjust)
                    self.pca9685.set_pwm(self.left_port, 0, self.position + self.left_adjust)
                else:
                    self.pca9685.set_pwm(self.right_port, 0, self.position + self.right_adjust)
                    self.pca9685.set_pwm(self.left_port, 0,
                                         toff_middle - self.position + self.left_adjust)
                sleep(max(seconds - time() + start, 0))

    def get_position(self):

        """
        Function to get the position of the articulation.

        Returns:
            degrees (int): The degrees of the position.
        """

        return round(180 / (self.max - self.min) * (self.position - self.min))

class Arm:

    """
    Class to control the full arm.

    Arguments:
        parameters (tuple): The tuple with 5 dictionaries with the articulation parameters:
            OneMotor (dict): The parameters of the base.
            TwoMotors (dict): The parameters of the shoulder.
            OneMotor (dict): The parameters of the elbow.
            OneMotor (dict): The parameters of the wrist.
            OneMotor (dict): The parameters of the wrench.
        position (tuple): The tuple with 5 positions to start in degrees:
            OneMotor (int): The parameters of the base. Default is 90.
            TwoMotors (int): The parameters of the shoulder. Default is 90.
            OneMotor (int): The parameters of the elbow. Default is 90.
            OneMotor (int): The parameters of the wrist. Default is 90.
            OneMotor (int): The parameters of the wrench. Default is 90.
        pca9685 (object): The PCA9685 object. Default is PCA9685().
        frequency (int): The frequency to be set. None for non set. Default is 50.

    Attributes:
        pca9685 (object): The PCA9685 object from pca9685 argument.
        base (object): The OneMotor object of the base.
        shoulder (object): The TwoMotors object of the shoulder.
        elbow (object): The OneMotor object of the elbow.
        wrist (object): The OneMotor object of the wrist.
        wrench (object): The OneMotor object of the wrench.
    """

    def __init__(self, parameters, positions=(90, 90, 90, 90, 90), pca9685=PCA9685(), frequency=50):
        self.pca9685 = pca9685
        if not frequency is None:
            self.pca9685.set_pwm_freq(frequency)
        self.base = OneMotor(parameters[0], positions[0], self.pca9685, None)
        self.shoulder = TwoMotors(parameters[1], positions[1], self.pca9685, None)
        self.elbow = OneMotor(parameters[2], positions[2], self.pca9685, None)
        self.wrist = OneMotor(parameters[3], positions[3], self.pca9685, None)
        self.wrench = OneMotor(parameters[4], positions[4], self.pca9685, None)

    def set_active(self, active=True):

        """
        Function to active or deactive the full arm.

        Arguments:
            active (bool): The boolean to activate or deactivate the full arm. Default is True.
        """

        self.base.set_active(active)
        self.shoulder.set_active(active)
        self.elbow.set_active(active)
        self.wrist.set_active(active)
        self.wrench.set_active(active)

    def is_active(self):

        """
        Function to get if all articulation status are active on the full arm.

        Returns:
            active (bool): The boolean which specifies if all the articulations are active.
        """

        return self.base.is_active() \
               and self.shoulder.is_active() \
               and self.elbow.is_active() \
               and self.wrist.is_active() \
               and self.wrench.is_active()

    def set_position(self, degrees, seconds=0):

        """
        Function to set the position for each articulation.

        Arguments:
            degrees (tuple): The tuple with 5 positions:
                OneMotor (int): The position of the base in degrees.
                TwoMotors (int): The position of the shoulder in degrees.
                OneMotor (int): The position of the elbow in degrees.
                OneMotor (int): The position of the wrist in degrees.
                OneMotor (int): The position of the wrench in degrees.
            seconds (float): The time in seconds to go to all positions set. Default is 0.
        """

        seconds = seconds / 5
        self.base.set_position(degrees[0], seconds)
        self.shoulder.set_position(degrees[1], seconds)
        self.elbow.set_position(degrees[2], seconds)
        self.wrist.set_position(degrees[3], seconds)
        self.wrench.set_position(degrees[4], seconds)

    def get_position(self):

        """
        Function to get the position of each articulation.

        Returns:
            degrees (tuple): The tuple with 5 positions:
                OneMotor (int): The position of the base in degrees.
                TwoMotors (int): The position of the shoulder in degrees.
                OneMotor (int): The position of the elbow in degrees.
                OneMotor (int): The position of the wrist in degrees.
                OneMotor (int): The position of the wrench in degrees.
        """

        return (self.base.get_position(),
                self.shoulder.get_position(),
                self.elbow.get_position(),
                self.wrist.get_position(),
                self.wrench.get_position())
