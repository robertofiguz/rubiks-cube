import cv2
import sys
import numpy as np
from imutils import contours
from collections import namedtuple

SQUARE_THRESHOLD = 150
FACE_WINDOW = "face"
WEBCAM_WINDOW = "camera"

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
    square_images = []
    square_colors = []
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
    
    face = camera if face_detected else None
    
    SQUARE = namedtuple('SQUARE', ['image','x', 'y', 'w', 'h'])
    for square in squares:
        if face is not None:
            # Detect the color of the square
            x, y, w, h = cv2.boundingRect(square)
            square_images.append(SQUARE(camera[y:y+h, x:x+w], x, y, w, h))
        cv2.drawContours(camera, [square], 0, (0, 255, 0), 2)
    

    for square in square_images:
        color = detect_square_color(square)
        square_colors.append(color)
        cv2.putText(camera, color, (square.x, square.y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    square_colors = square_colors[::-1]
    
    return camera, face

# TODO: This function needs improvement
def detect_square_color(square):
    #FIXME: Use calibrated values for the range of colors
    hsv = cv2.cvtColor(square.image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    h = h.flatten()
    s = s.flatten()
    v = v.flatten()
    h = h[h > 0]
    s = s[s > 0]
    v = v[v > 0]
    h = np.mean(h)
    s = np.mean(s)
    v = np.mean(v)
    if h < 10:
        return 'R'
    elif 10 < h < 25:
        return 'O'
    elif 25 < h < 35:
        return 'Y'
    elif 35 < h < 77:
        return 'G'
    elif 77 < h < 99:
        return 'B'
    elif 99 < h < 124:
        return 'W'
    return 'NA'

def init_windows():
    cv2.namedWindow(FACE_WINDOW)
    cv2.moveWindow(FACE_WINDOW, 1200, 0)

    cv2.namedWindow(WEBCAM_WINDOW)
    cv2.moveWindow(WEBCAM_WINDOW, 0, 0)

    face_background = np.zeros((480, 640, 3), np.uint8)
    cv2.putText(face_background, "When a cube face is detected it will be displayed here", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    cv2.imshow(FACE_WINDOW, face_background)
        
def main():

    init_windows()

    video = cv2.VideoCapture(0)
    is_ok, bgr_image_input = video.read()
    
    if not is_ok:
        print("Cannot read video source")
        sys.exit()
    
    while True:
        _, camera = video.read()

        # camera = cv2.imread("resources/cube-face.jpg")

        camera, face = detect_cube_face(camera)


        cv2.imshow(WEBCAM_WINDOW, camera)
        if face is not None:
            cv2.imshow(FACE_WINDOW, face)

        key_pressed = cv2.waitKey(1) & 0xFF
        if key_pressed == 27 or key_pressed == ord('q'):
            break


if __name__ == "__main__":
    main()