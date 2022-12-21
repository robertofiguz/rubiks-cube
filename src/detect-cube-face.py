import cv2
import sys
import numpy as np
from imutils import contours


def mask_cube_face(camera):
    ''' Adapted from: https://stackoverflow.com/questions/24916870/python-opencv-rubiks-cube-solver-color-extraction
        Detects the cube face and returns the masked image
    '''
    # Define the color ranges
    colors = {
        'white': ([0, 0, 168], [172, 111, 255]),      
        'blue': ([69, 120, 100], [179, 255, 255]),    
        'yellow': ([21, 110, 117], [45, 255, 255]),  
        'orange': ([0, 110, 125], [17, 255, 255]),    
        'red': ([0, 50, 50], [10, 255, 255]),         
        'green': ([40, 40, 40], [70, 255, 255])       
        }

    image = cv2.cvtColor(camera, cv2.COLOR_BGR2HSV)
    mask = np.zeros(image.shape, dtype=np.uint8)

    # Remove noise from the squares
    open_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
    close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))

    # Build a mask based on the color ranges
    for color, (lower, upper) in colors.items():
        lower = np.array(lower, dtype=np.uint8)
        upper = np.array(upper, dtype=np.uint8)
        color_mask = cv2.inRange(image, lower, upper)
        color_mask = cv2.morphologyEx(color_mask, cv2.MORPH_OPEN, open_kernel, iterations=1)
        color_mask = cv2.morphologyEx(color_mask, cv2.MORPH_CLOSE, close_kernel, iterations=5)

        # Merging all calculated masks TODO: separate them to detect each color
        color_mask = cv2.merge([color_mask, color_mask, color_mask])
        mask = cv2.bitwise_or(mask, color_mask)

    gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    cnts = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    # Sort all contours from top-to-bottom or bottom-to-top
    (cnts, _) = contours.sort_contours(cnts, method="top-to-bottom")

    # Take each row of 3 and sort from left-to-right or right-to-left
    cube_rows = []
    row = []
    for (i, c) in enumerate(cnts, 1):
        row.append(c)
        if i % 3 == 0:  
            (cnts, _) = contours.sort_contours(row, method="left-to-right")
            cube_rows.append(cnts)
            row = []

    # Draw rectangles around the squares
    for row in cube_rows:
        for c in row:
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(camera, (x, y), (x + w, y + h), (36,255,12), 2)
    return camera, mask


def main():
    video = cv2.VideoCapture(0)
    is_ok, bgr_image_input = video.read()
    
    if not is_ok:
        print("Cannot read video source")
        sys.exit()
    
    while True:
        _, camera = video.read()

        camera = cv2.imread("resources/cube-face.jpg")

        camera, mask = mask_cube_face(camera)
                
        # gray = cv2.cvtColor(camera,cv2.COLOR_BGR2GRAY)

        # binary = cv2.adaptiveThreshold(gray,20,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,5,0)


        # try:
        #  _, contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        # except:
        #     contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

        # for contour in contours:
        #     area = cv2.contourArea(contour)
        #     if not (area < 1500 and area > 1000):
        #         continue
        #     perimeter = cv2.arcLength(contour, True)
        #     epsilon = 0.01 * perimeter
        #     approx = cv2.approxPolyDP(contour, epsilon, True)
        #     hull = cv2.convexHull(contour)
        #     x, y, w, h = cv2.boundingRect(contour)

        #     cv2.drawContours(camera,[contour],0,(255, 255, 0),2)
        #     cv2.drawContours(camera, [approx], 0, (255, 255, 0), 2)

        cv2.imshow("camera", camera)
        #cv2.imshow("binary", binary)
        cv2.imshow("mask", mask)
        key_pressed = cv2.waitKey(1) & 0xFF
        if key_pressed == 27 or key_pressed == ord('q'):
            break


if __name__ == "__main__":
    main()