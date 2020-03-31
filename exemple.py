# -*- coding: utf-8 -*-

"""
Exemple to control the Robotic Arm with robotic_arm module: https://github.com/MPi3D/Robotic_Arm.
"""

from time import sleep
from robotic_arm import Arm # Import the Arm class.

PARMS = (
    {"Port": 0, "Adjust": 5, "Min": 130, "Max": 475, "Reverse": True}, # Base parameters.
    {"Left Port": 1, "Right Port": 2,
     "Left Adjust": 20, "Min": 130, "Max": 475, "Reverse": True}, # Shoulder parameters.
    {"Port": 3, "Adjust": -5, "Min": 150, "Max": 500, "Reverse": True}, # Elbow parameters.
    {"Port": 4, "Adjust": -5, "Min": 125, "Max": 540, "Reverse": True}, # Wrist parameters.
    {"Port": 5, "Min": 280, "Max": 450} # Wrench parameters.
)

ARM = Arm(PARMS, (90, 90, 0, 90, 90)) # Init the arm with the PARMS.

ARM.base.set_position(0) # Set the base to 0 degree.

ARM.base.set_position(180, 5) # Set the base to 180 degrees in 5 seconds.

ARM.set_position((90, 90, 90, 0, 0)) # Set full arm to the position (90, 90, 90, 0, 0).
ARM.set_active(False) # Set the full arm deactivate.
sleep(5)

ARM.elbow.set_position(180, 2) # Set the elbow to 180 degrees in 2 seconds.
print(ARM.is_active()) # Get if all articulations of the arm are active.

ARM.shoulder.set_position(0, 2) # Set the shoulder to 180 degrees in 5 seconds.
ARM.shoulder.set_active(False) # Set the shoulder deactivate.
sleep(2)

print(ARM.base.is_active()) # Get if the base is active.
ARM.set_active() # Set all articulations of the arm to active.
sleep(2)

ARM.set_position((90, 90, 90, 90, 90), 5) # Set full arm to the position (90, 90, 90, 90, 90)
                                          # in 5 seconds.
ARM.set_active(False) # Set all articulations of the arm to deactivate.
