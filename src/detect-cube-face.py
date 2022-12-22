import cv2
import sys
import numpy as np
from imutils import contours

SQUARE_THRESHOLD = 150

def detect_cube_face(camera):
    ''' Detects the cube face and square colors
    '''
    face_detected = False

    gray = cv2.cvtColor(camera,cv2.COLOR_BGR2GRAY)
    binary = cv2.adaptiveThreshold(gray,20,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,5,0)

    try:
        _, contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    except ValueError:
        contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    
    squares = []
    for contour in contours:
        area = cv2.contourArea(contour)

        if not (1000<area<3000):
            continue

        perimeter = cv2.arcLength(contour, True)
        if cv2.norm(((perimeter / 4) * (perimeter / 4)) - area) < SQUARE_THRESHOLD:
            #if it is a square form
            squares.append(contour)

    if len(squares) != 9:
        if len(squares) == 0:
            cv2.putText(camera, "No face detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        elif len(squares) > 9:
            cv2.putText(camera, "Detecting more than 9 squares. \nTry to remove noise in the background", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        elif len(squares) < 9:
            cv2.putText(camera, "Not able to detect all the 9 squares", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 215, 255), 2)
    else:
        face_detected = True
        cv2.putText(camera, "Face detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    for square in squares:
        cv2.drawContours(camera, [square], 0, (0, 255, 0), 2)

    face = camera if face_detected else None

    return camera, face

def main():
    video = cv2.VideoCapture(0)
    is_ok, bgr_image_input = video.read()
    
    if not is_ok:
        print("Cannot read video source")
        sys.exit()
    
    while True:
        _, camera = video.read()

        # camera = cv2.imread("resources/cube-face.jpg")

        camera, face = detect_cube_face(camera)

        # try:
        #     camera, mask = mask_cube_face(camera)
        # except ValueError:
        #     print("No face detected")
        #     continue    


        cv2.imshow("camera", camera)
        if face is not None:
            cv2.imshow("face", face)
        #cv2.imshow("binary", binary)
        #cv2.imshow("mask", mask)
        key_pressed = cv2.waitKey(1) & 0xFF
        if key_pressed == 27 or key_pressed == ord('q'):
            break


if __name__ == "__main__":
    main()