#!/usr/bin/env python3

import time


def move_forward(duration):
    print("Moving forward for", duration, "seconds")
    time.sleep(duration)


def turn_left(duration):
    print("Turning left for", duration, "seconds")
    time.sleep(duration)


def stop_robot():
    print("Stopping robot")
    time.sleep(1)


def main():
    forward_time = 2.0
    turn_time = 1.0

    print("Starting open loop square movement")

    for side in range(4):
        print("Side", side + 1)
        move_forward(forward_time)
        turn_left(turn_time)

    stop_robot()
    print("Open loop square movement finished")


if __name__ == "__main__":
    main()
