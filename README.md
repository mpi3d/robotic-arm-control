# Robotic Arm Control

Program to control the [Robotic Arm](https://github.com/MPi3D/Robotic_Arm) and record the programs

[![Robotic Arm](/Robotic_Arm.jpg)](https://github.com/MPi3D/Robotic_Arm)

## Program

+ [Program](/Robotic_Arm.py)

## Install

```
chmod +x install.sh
sudo install.sh
```

## Usage

```
from Robotic_Arm import Arm

PARMS = (
    {"Port": 0, "Adjust": 5, "Min": 130, "Max": 475, "Reverse": True}, # Base
    {"Left Port": 1, "Right Port": 2, "Left Adjust": 20, "Min": 130, "Max": 475, "Reverse": True}, # Shoulder
    {"Port": 3, "Adjust": -5, "Min": 150, "Max": 500, "Reverse": True}, # Elbow
    {"Port": 4, "Adjust": -5, "Min": 125, "Max": 540, "Reverse": True}, # Wrist
    {"Port": 5, "Min": 280, "Max": 450} # Wrench
)

ARM = Arm(PARMS)

ARM.activate(False)
```
