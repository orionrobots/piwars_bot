# OO approach, but is derived from PiBorgs JoyBorg code
import time
import pygame
import logging
import skittlebot

logger = logging.getLogger(__file__)

# Constants

AXIS_UP_DOWN = 1
AXIS_LEFT_RIGHT = 3
AXIS_UP_DOWN_INVERTED = False
AXIS_LEFT_RIGHT_INVERTED = False

# We have our robot class
# There is an event loop - to read events from pygame, and process them.

def read_axis(joystick, axis_number, inverted, dead_threshold):
    reading = joystick.get_axis(axis_number)
    if inverted:
        reading = -reading
    if reading > dead_threshold or -reading > dead_threshold:
        return reading
    else:
        return 0

class JoypadRobot(object):
    def __init__(self, robot):
        """Robot is a object, with motor L speed, motor R speed"""
        self.robot = robot
        self.interval = 0.1 # 100 millis
        self.joystick = None

    def handle_joystick_movement(self, up_down, left_right):
        # This is not really right yet.. 
        left_speed = up_down + left_right
        right_speed = up_down - left_right
        # Limit to -1.0 - 0 - 1.0
        if left_speed > 1.0:
            left_speed = 1.0
        elif left_speed < -1.0:
            left_speed = -1.0
        if right_speed > 1.0:
            right_speed = 1.0
        elif right_speed < -1.0:
            right_speed = -1.0
        robot.set_motors(left_speed, right_speed)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.JOYAXISMOTION:
                # Joystick event - move the robot
                up_down = read_axis(joystick, AXIS_UP_DOWN, AXIS_UP_DOWN_INVERTED, 0.1)
                left_right = read_axis(joystick, AXIS_LEFT_RIGHT, AXIS_LEFT_RIGHT_INVERTED, 0.1)
                self.handle_joystick_movement(up_down, left_right)


    def run(self):
        logger.debug("Initialising pygame")
        pygame.init()
        pygame.joystick.init()
        logger.debug("Creating joystick instance")
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        logger.debug("Pygame ready")

        while True:
            self.handle_events(pygame.event.get())
            time.sleep(self.interval)

def main():
    with skittlebot.Robot() as robot:
        jp_robot = JoypadRobot(robot)
        jp_robot.run()


if __name__ == '__main__':
    main()