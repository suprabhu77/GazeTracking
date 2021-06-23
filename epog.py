#!/usr/bin/env python3


"""
Demonstration of how to use the eye point of gaze (EPOG) tracking library.

This example application can be called like this (both args are optional):
>> ./epog_example.py 1 'log_file_prefix'

'1': stabilize estimated EPOG w.r.t. previous cluster of EPOGs
'0': allow spurious EPOGs that deviate from cluster (default)

'log_file_prefix': (e.g. user_id) A logfile will be created with the errors, i.e.
the Euclidean distance (in pixels) between test points and corresponding estimated EPOGs.
Log file will be e.g. test_errors/'log_file_prefix'_stab_01-12-2019_18.36.44.txt
If log_file_prefix is omitted, log file will not be created.

Check the README.md for complete documentation.
"""

import sys
import cv2
import gaze_tracking as gt
import pyautogui as gui
from collections import deque
gui.FAILSAFE = False
# setup_epog expects max two args, both optional,
# sets up webcam, and calibration windows
test_error_dir = '../GazeEvaluation/test_errors/'
epog = gt.EPOG(test_error_dir, sys.argv)

queueSize = 5

X_COORDINATES = deque(list(map(int, list("0"*queueSize))))
Y_COORDINATES = deque(list(map(int, list("0"*queueSize))))


def add_coordinates_and_return(x, y):
    global X_COORDINATES, Y_COORDINATES
    X_COORDINATES.append(x)
    Y_COORDINATES.append(y)

    X_COORDINATES.popleft()
    Y_COORDINATES.popleft()

    return int(sum(X_COORDINATES)/len(X_COORDINATES)), int(sum(Y_COORDINATES)/len(Y_COORDINATES))


while True:
    # We get a new frame from the webcam
    _, frame = epog.webcam.read()
    if frame is not None:
        # Analyze gaze direction and map to screen coordinates
        screen_x, screen_y = epog.analyze(frame)
        # screen_x,screen_y = gui.position()

        # Access gaze direction
        text = ""
        
        if epog.gaze_tr.is_right():
            text = "Looking right"
        elif epog.gaze_tr.is_left():
            text = "Looking left"
        elif epog.gaze_tr.is_center():
            text = "Looking center"
        elif epog.gaze_tr.is_blinking():
            text = "clicking"
            print(text)

        # Use gaze projected onto screen surface
        # Screen coords will be None for a few initial frames,
        # before calibration and tests have been completed
        
        if screen_x is not None and screen_y is not None:
            text = "Looking at point {}, {} on the screen".format(
                screen_x, screen_y)
            print(text)
            x, y = add_coordinates_and_return(screen_x, screen_y)
            print(x, y)
            gui.moveTo(x, y, duration=0.1)
        

        # Press Esc to quit the video analysis loop
        if cv2.waitKey(1) == 27:
            # Release video capture
            epog.webcam.release()
            cv2.destroyAllWindows()
            break
        # Note: The waitkey function is the only method in HighGUI that can fetch and handle events,
        # so it needs to be called periodically for normal event processing unless HighGUI
        # is used within an environment that takes care of event processing.
        # Note: The waitkey function only works if there is at least one HighGUI window created and
        # the window is active. If there are several HighGUI windows, any of them can be active.
        # (https://docs.opencv.org/2.4/modules/highgui/doc/user_interface.html)
#add