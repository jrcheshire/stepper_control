# stepper_control
Arduino-based stepper motor control using Python

This program can rotate a stepper motor by a given angle, or at a given speed (in degrees per second) for a given number of rotations. Maximum speed and degree/step values are based on a Newport UE63PP stepper motor, feel free to change these to correspond to your equipment.

Usage:
python rotator.py -r <angle>
python rotator.py -r <speed,#rotations>

E.g.: python rotator.py -r 15,5
