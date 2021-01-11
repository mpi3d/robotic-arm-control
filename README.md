# Robotic Arm Control

Program to control the [Robotic Arm](https://github.com/mpi3d/robotic-arm).

[![Robotic Arm](/robotic_arm.jpg)](https://github.com/mpi3d/robotic-arm)

## Install

``` sh
git clone https://github.com/mpi3d/robotic-arm-control.git
cd robotic-arm-control
chmod +x install.sh
sudo install.sh
```

## Program

+ [Program](/robotic_arm.py)

## Exemple

+ [Exemple](/exemple.py)

## Usage

``` python
from robotic_arm import * # Import the OneMotor, TwoMotors and Arm class.

PARMS = (
    {"Port": 0, "Adjust": 5, "Min": 130, "Max": 475, "Reverse": True}, # Base parameters.
    {"Left Port": 1, "Right Port": 2,
     "Left Adjust": 20, "Min": 130, "Max": 475, "Reverse": True}, # Shoulder parameters.
    {"Port": 3, "Adjust": -5, "Min": 150, "Max": 500, "Reverse": True}, # Elbow parameters.
    {"Port": 4, "Adjust": -5, "Min": 125, "Max": 540, "Reverse": True}, # Wrist parameters.
    {"Port": 5, "Min": 280, "Max": 450} # Wrench parameters.
)

ARM = Arm(PARMS) # Init the arm with the PARMS.

# base can be replace by shoulder, elbow, wrist or wrench.

ARM.base.set_position(90) # Set the base to 90 degrees.
ARM.base.set_position(90, 5) # Set the base to 90 degrees in 5 seconds.

ARM.base.set_active(False) # Set the base deactivate.
ARM.base.set_active(True) # Set the base activate.

ARM.base.is_active() # Get if base is active.
ARM.base.get_position() # Get base positions.

ARM.set_position((90, 90, 90, 90, 90)) # Set full arm to the position (90, 90, 90, 90, 90).
ARM.set_position((90, 90, 90, 90, 90), 5) # Set full arm to the position (90, 90, 90, 90, 90)
                                          # in 5 seconds.

ARM.set_active(False) # Set the full arm deactivate.
ARM.set_active(True) # Set the full arm activate.

ARM.is_active() # Get if all articulations of the arm are active.
ARM.get_position() # Get all articulations positions.

help(Arm) # To get more informations about Arm class.
help(OneMotor) # To get more informations about OneMotor class.
help(TwoMotors) # To get more informations about TwoMotors class.
```
