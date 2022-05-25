from adafruit_servokit import ServoKit
from HardwareConstants import JoystickConstants
import time

class Servomotor:
    """Servomotors class

    This class manages the servomotors used to move the camera
    """
    CHANNEL = 16
    VERTICAL = 0
    HORIZONTAL = 1
    angle_min, angle_max = 0, 180
    step = 3

    def __init__(self):
        self.kit = ServoKit(channels=self.CHANNEL)
        self.kit.servo[self.HORIZONTAL].angle = 90
        self.kit.servo[self.VERTICAL].angle = 90

    def turnLeft(self):
        """Move horizontal servomotor to the left
        """
        if self.kit.servo[self.HORIZONTAL].angle < self.angle_max - self.step:
            self.kit.servo[self.HORIZONTAL].angle += self.step

    def turnRight(self):
        """Move horizontal servomotor to the right
        """
        if self.kit.servo[self.HORIZONTAL].angle > self.angle_min + self.step:
            self.kit.servo[self.HORIZONTAL].angle -= self.step


    def goDown(self):
        """Move vertical servomotor down
        """
        if self.kit.servo[self.VERTICAL].angle > self.angle_min + self.step:
            self.kit.servo[self.VERTICAL].angle -= self.step

    def goUp(self):
        """Move vertical servomotor up
        """
        if self.kit.servo[self.VERTICAL].angle < self.angle_max - self.step:
            self.kit.servo[self.VERTICAL].angle += self.step

    def update_servo(self, state):
        """Update servo motors based on joystick state

        Positional argument:
        state -- state of the joystick
        """
        if state ==JoystickConstants.JS_MIDDLE:
            return
        if state == JoystickConstants.JS_UP:
            self.goUp()
        elif state == JoystickConstants.JS_DOWN:
            self.goDown()
        elif state == JoystickConstants.JS_RIGHT:
            self.turnRight()
        elif state == JoystickConstants.JS_LEFT:
            self.turnLeft()
