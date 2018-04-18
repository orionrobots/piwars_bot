"""Wall avoiding"""
from piwars_bot import Robot
from piwars_bot_controller import PiWarsController

forward_speed = 100
reverse_speed  = -50
forward_react_dist = 10
def main():
    mode = 'Waiting for first reading'
    with Robot() as robot: #, PiWarsController().connect_pad() as joystick:
        while True: #joystick.connected and not joystick['home']:
            # of left, right and forward - which is furthest?
            left = robot.left_distance
            forward = robot.forward_distance
            right = robot.right_distance
            print(left, forward, right, mode)
            if mode == 'turning right' and forward < forward_react_dist:
                robot.set_right(reverse_speed)
            elif mode == 'turning left' and forward < forward_react_dist:
                robot.set_left(reverse_speed)
            elif forward > forward_react_dist:
                robot.set_left(forward_speed)
                robot.set_right(forward_speed)
                mode = 'forward'
            else:
                if left < right:
                    mode = 'turning left'
                    robot.set_left(reverse_speed)
                else:
                    mode = 'turning right'
                    robot.set_right(reverse_speed)

if __name__ == '__main__':
    main()
