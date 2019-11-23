# Robotic Arm Control

Program to control the [Robotic Arm](https://github.com/MPi3D/Robotic_Arm) and record the programs

[![Robotic Arm](/Robotic_Arm.jpg)](https://github.com/MPi3D/Robotic_Arm)

## Program

+ [Program](/Robotic_Arm.py)

## Usage

```
from Robotic_Arm import *

arm = Arm()
arm.set_degrees(base, 180)
arm.set_degrees(elbow, 90)
arm.set_disable(all)
```
