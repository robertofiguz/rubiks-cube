from copy import deepcopy
import cv2
import sys
import json
import kociemba
import numpy as np
from imutils import contours
from collections import namedtuple
import animate_cube as animate

TEXT_PROMPTS = {1: "Show the white face with the green on top", 
                2: "Rotate the cube 90 to the right",
                3: "Rotate the cube 90 to the right",
                4: "Rotate the cube 90 to the right",
                5: "Rotate the cube 90 to the right and 90 up",
                6: "Rotate the cube 180 down",
                7: ""}
FACES = {}
SQUARE_THRESHOLD = 150
FACE_WINDOW = "face"
WEBCAM_WINDOW = "camera"

def detect_cube_face(camera):
    ''' Detects the cube face and square colors
    '''
    SQUARE = namedtuple('SQUARE', ['image','x', 'y', 'w', 'h'])
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
        if cv2.norm((perimeter / 4) ** 2 - area) < SQUARE_THRESHOLD:
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
    
    for square in squares:
        if face is not None:
            # Detect the color of the square
            x, y, w, h = cv2.boundingRect(square)
            square_images.append(SQUARE(camera[y:y+h, x:x+w], x, y, w, h))
        cv2.drawContours(camera, [square], 0, (0, 255, 0), 2)
    
    with open("resources/color-calibration.json", "r") as f:
        color_calibration = json.load(f)

    count = 1
    square_images = sorted(square_images, key=lambda square: (square.y, square.x), reverse=False)
    for square in square_images:
        color = detect_square_color(square, color_calibration)
        square_colors.append(color)
        cv2.circle(camera, (square.x + square.w // 2, square.y + square.h // 2), 5, (0, 0, 255), -1)
        cv2.putText(camera, str(count)+'-'+color, (square.x, square.y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        count +=1
    
    return camera, face, square_colors

def get_dominant_color(image):
    ''' Returns the dominant color of the square
    '''

    #FIXME: Getting better results without using this function

    data = np.reshape(image, (-1,3))
    data = np.float32(data)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    compactness,labels,centers = cv2.kmeans(data,1,None,criteria,10,flags)

    dominant_color = centers[0].astype(np.int32)

    return dominant_color[0].astype(np.int32), dominant_color[1].astype(np.int32), dominant_color[2].astype(np.int32)

def detect_square_color(square, color_ranges):
    b, g, r = square.image[square.w // 2, square.h // 2]
    
    for color, color_range in color_ranges.items():
        if color_range['B']['min'] < b < color_range['B']['max'] \
            and color_range['G']['min'] < g < color_range['G']['max'] \
                and color_range['R']['min'] < r < color_range['R']['max']:
            return color
    return "unk"

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
    is_ok, camera = video.read()
    
    if not is_ok:
        print("Cannot read video source")
        sys.exit()

    while True:
        _, camera = video.read()

        # camera = cv2.imread("resources/cube-face.jpg")

        camera, face, squares = detect_cube_face(camera)


        cv2.putText(camera, TEXT_PROMPTS[len(FACES)+1], (20, camera.shape[0]-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        cv2.imshow(WEBCAM_WINDOW, camera)
        FACES = ["F", "R", "B", "L", "U", "D"]
        if face is not None and len(FACES) < 6:
            cv2.imshow(FACE_WINDOW, face)
            # Uncomment this lines
            # if "unk"  in squares:
            #     continue
            key_pressed = cv2.waitKey(0) & 0xFF
            if key_pressed == 27 or key_pressed == ord('q'):
                continue
            elif key_pressed == 13: #ENTER
                FACES[squares[4]] = squares
                print(f"Saved {squares[4]} Face: ", squares)
        elif face is not None: # The cube is detected
            face_background = np.zeros((480, 640, 3), np.uint8)
            cv2.putText(face_background, "The cube was fully detected", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.imshow(FACE_WINDOW, face)

            cube_string = ("".join(FACES["G"]) + "".join(FACES["R"]) + "".join(FACES["W"]) + "".join(FACES["O"]) + "".join(FACES["Y"]) + "".join(FACES["B"]))

            cube_string = "GGGGGGGGGRRRRRRRRRWWWWWWWWWBBBBBBBBBOOOOOOOOOYYYYYYYYY"

            kociemba_string = deepcopy(cube_string)
            kociemba_string.replace("G", "U")
            kociemba_string.replace("R", "R")
            kociemba_string.replace("W", "F")
            kociemba_string.replace("O", "L")
            kociemba_string.replace("Y", "B")
            kociemba_string.replace("B", "D")

            print("Solving the cube...")
            solution = kociemba.solve(kociemba_string)
            animate.main(cube_string, solution)


        key_pressed = cv2.waitKey(1) & 0xFF
        if key_pressed == 27 or key_pressed == ord('q'):
            break


if __name__ == "__main__":
    main()