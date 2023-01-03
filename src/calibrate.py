#!/usr/bin/env python3


# Imports
import sys
import cv2
import numpy as np
import json
from functools import partial
from numpy import mean
COLORS = {"White": (255, 255, 255), "Yellow": (0, 255, 255), "Orange": (0, 165, 255), "Red": (0, 0, 255), "Green": (0, 255, 0), "Blue": (255, 0, 0)}


def getLimits(window_name):
    min_b = cv2.getTrackbarPos('min B', window_name)
    min_g = cv2.getTrackbarPos('min G', window_name)
    min_r = cv2.getTrackbarPos('min R', window_name)

    max_b = cv2.getTrackbarPos('max B', window_name)
    max_g = cv2.getTrackbarPos('max G', window_name)
    max_r = cv2.getTrackbarPos('max R', window_name)

    min = np.array([min_b, min_g, min_r], np.uint8)
    max = np.array([max_b, max_g, max_r], np.uint8)

    return min, max


def onTrackbar(val):    # replaced by getLimits() but
    pass                # required to create trackbars


def mouseClick(event, x, y, flags, param, window_name, img_dict):

    if event == cv2.EVENT_LBUTTONDOWN:
        
        image = img_dict['image']
        b, g, r = image[y, x]
    
        range = 30

        min_b = b - range if b > range else 0
        max_b = b + range if b < 255-range else 255
        min_g = g - range if g > range else 0
        max_g = g + range if g < 255-range else 255
        min_r = r - range if r > range else 0
        max_r = r + range if r < 255-range else 255

        limits = {'min B': min_b, 'max B': max_b, 'min G': min_g, 'max G': max_g, 'min R': min_r, 'max R': max_r}

        for limit in limits:
            cv2.setTrackbarPos(limit, window_name, limits[limit])


def run(colors_class):
    

    # Create windows
    name_segmented = 'Segmented'
    name_original = 'Original'
    cv2.namedWindow(name_segmented, cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow(name_original, cv2.WINDOW_AUTOSIZE)



    limits = {'B': {'max': 200, 'min': 100}, 'G': {'max': 200, 'min': 100}, 'R': {'max': 200, 'min': 100}}


    # Create trackbars {'name': count}
    trackbars = {'min B': limits['B']['min'],
                    'max B': limits['B']['max'],
                    'min G': limits['G']['min'],
                    'max G': limits['G']['max'],
                    'min R': limits['R']['min'],
                    'max R': limits['R']['max']}

    for tb in trackbars:
        cv2.createTrackbar(tb, name_segmented, trackbars[tb], 255, onTrackbar)


    # Select camera and get first frame
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    _, image = capture.read()
    #image = cv2.flip(image, 1)
    img_dict = {'image': image}


    # Move windows to starting pos
    cv2.moveWindow(name_original, 100, 0)
    cv2.moveWindow(name_segmented, image.shape[1] + 120, 0)


    # Create mouse callback
    cv2.setMouseCallback(name_original, partial(mouseClick, window_name=name_segmented, img_dict=img_dict))



    dict = {}
    colors = {"W": "White", "B": "Blue", "G": "Green", "R": "Red", "Y": "Yellow", "O": "Orange"}
    color_names = ["W", "B", "G", "R", "Y", "O"]
    color_calibrated = False
    color = color_names.pop(0)
    while True:

        if color_calibrated:
            color = color_names.pop(0)
            color_calibrated = False
        
        # Update image from camera
        _, image = capture.read()
        #image = cv2.flip(image, 1)
        img_dict['image'] = image
        cv2.putText(image, f"Let's Calibrate {colors[color]} color", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[colors[color]], 2)
        cv2.imshow(name_original, image)


        # Update segmented image
        min, max = getLimits(name_segmented)
        image_thresholded = cv2.inRange(image, min, max)
        cv2.imshow(name_segmented, image_thresholded)


        # Keyboard inputs
        key = cv2.waitKey(10) & 0xFF        # Only read last byte (prevent numlock)

        if key == ord('w') or key == 13:    # w or ENTER
            min = min.tolist()
            max = max.tolist()

            dict[color] = {'B': {'max': max[0], 'min': min[0]},
                                'G': {'max': max[1], 'min': min[1]},
                                'R': {'max': max[2], 'min': min[2]}}

            if color == "O":
                for i in dict:
                    color = colors[i]
                    values = dict[i]
                    max = (values['B']['max'], values['G']['max'], values['R']['max'])
                    min = (values['B']['min'], values['G']['min'], values['R']['min'])
                    print(f"{color} max: {max} min: {min}")
                    average = (mean([max[0], min[0]]), mean([max[1], min[1]]), mean([max[2], min[2]]))
                    colors_class.update_prominent_color(color.lower(), average)
                cv2.destroyAllWindows()
                return
            color_calibrated = True

        elif key == ord('q') or key == 27:  # q or ESC
            sys.exit(0)




if __name__ == '__main__':
    run()