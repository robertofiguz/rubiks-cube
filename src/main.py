import cv2
import time
from predict import predicted_color
import numpy as np
from draw import draw_2d_cube_state
class Face:
    def __init__(self, name):
        self.face = [[None,None,None],
                     [None,None,None],
                     [None,None,None]]

        print(self.face)
        self.name = name
        self.scanned = False
    def update(self, index, color):
        if not self.scanned:
            col = index % 3
            row = index // 3
            self.face[row][col] = color
            if None not in self.face[0] and None not in self.face[1] and None not in self.face[2]:
                self.scanned = True
                print('Face {} scanned!'.format(self.name))
    def flatten(self):
        return [color for row in self.face for color in row]
    def get_face(self):
        #print a 3x3 grid text representation of the face
        text = '| {} | {} | {} |\n| {} | {} | {} |\n| {} | {} | {} |\n'.format(*self.flatten())
        
        #make tree rows with equal length columns for each color
        rows = text.split('\n')
        rows = [row.split('|') for row in rows]
        rows = [[col.strip() for col in row] for row in rows]
        rows = [[col.ljust(10) for col in row] for row in rows]
        rows = ['|'.join(row) for row in rows]
        text = '\n'.join(rows)
        #make text color coded
        text = text.replace('red', '\033[91mred\033[0m')
        text = text.replace('orange', '\033[93morange\033[0m')
        text = text.replace('blue', '\033[94mblue\033[0m')
        text = text.replace('green', '\033[92mgreen\033[0m')
        text = text.replace('white', '\033[97mwhite\033[0m')
        text = text.replace('yellow', '\033[93myellow\033[0m')


        return text
    def is_scanned(self):
        return self.scanned

def find_contours( dilatedFrame):
    contours, hierarchy = cv2.findContours(dilatedFrame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    final_contours = []
    # Step 1/4: filter all contours to only those that are square-ish shapes.
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.1 * perimeter, True)
        if len (approx) == 4:
            area = cv2.contourArea(contour)
            (x, y, w, h) = cv2.boundingRect(approx)
            # Find aspect ratio of boundary rectangle around the countours.
            ratio = w / float(h)
            # Check if contour is close to a square.
            if ratio >= 0.8 and ratio <= 1.2 and w >= 30 and w <= 60 and area / (w * h) > 0.4:
                final_contours.append((x, y, w, h))
    # Return early if we didn't found 9 or more contours.
    if len(final_contours) < 9:
        return final_contours
    # Step 2/4: Find the contour that has 9 neighbors (including itself)
    # and return all of those neighbors.
    found = False
    contour_neighbors = {}
    for index, contour in enumerate(final_contours):
        (x, y, w, h) = contour
        contour_neighbors[index] = []
        center_x = x + w / 2
        center_y = y + h / 2
        radius = 1.5
        # Create 9 positions for the current contour which are the
        # neighbors. We'll use this to check how many neighbors each contour
        # has. The only way all of these can match is if the current contour
        # is the center of the cube. If we found the center, we also know
        # all the neighbors, thus knowing all the contours and thus knowing
        # this shape can be considered a 3x3x3 cube. When we've found those
        # contours, we sort them and return them.
        neighbor_positions = [
            # top left
            [(center_x - w * radius), (center_y - h * radius)],
            # top middle
            [center_x, (center_y - h * radius)],
            # top right
            [(center_x + w * radius), (center_y - h * radius)],
            # middle left
            [(center_x - w * radius), center_y],
            # center
            [center_x, center_y],
            # middle right
            [(center_x + w * radius), center_y],
            # bottom left
            [(center_x - w * radius), (center_y + h * radius)],
            # bottom middle
            [center_x, (center_y + h * radius)],
            # bottom right
            [(center_x + w * radius), (center_y + h * radius)],
        ]
        for neighbor in final_contours:
            (x2, y2, w2, h2) = neighbor
            for (x3, y3) in neighbor_positions:
                # The neighbor_positions are located in the center of each
                # contour instead of top-left corner.
                # logic: (top left < center pos) and (bottom right > center pos)
                if (x2 < x3 and y2 < y3) and (x2 + w2 > x3 and y2 + h2 > y3):
                    contour_neighbors[index].append(neighbor)
    # Step 3/4: Now that we know how many neighbors all contours have, we'll
    # loop over them and find the contour that has 9 neighbors, which
    # includes itself. This is the center piece of the cube. If we come
    # across it, then the 'neighbors' are actually all the contours we're
    # looking for.
    for (contour, neighbors) in contour_neighbors.items():
        if len(neighbors) == 9:
            found = True
            final_contours = neighbors
            break
    if not found:
        return []
    # Step 4/4: When we reached this part of the code we found a cube-like
    # contour. The code below will sort all the contours on their X and Y
    # values from the top-left to the bottom-right.
    # Sort contours on the y-value first.
    y_sorted = sorted(final_contours, key=lambda item: item[1])
    # Split into 3 rows and sort each row on the x-value.
    top_row = sorted(y_sorted[0:3], key=lambda item: item[0])
    middle_row = sorted(y_sorted[3:6], key=lambda item: item[0])
    bottom_row = sorted(y_sorted[6:9], key=lambda item: item[0])
    sorted_contours = top_row + middle_row + bottom_row
    return sorted_contours

def draw_contours(frame,contours):
    """Draw contours onto the given frame."""
    for index, (x, y, w, h) in enumerate(contours):
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255,0,255), 2)
    return frame

def all_scanned(faces):
    """Check if all faces have been scanned."""
    for face in faces.values():
        if not face.scanned:
            return False
    return True

#start camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
time.sleep(1)
frame1 = []
frame1_contours = []

faces ={
    'red': Face('red'),
    'green': Face('green'),
    'blue': Face('blue'),
    'yellow': Face('yellow'),
    'orange': Face('orange'),
    'white': Face('white')
}

while not all_scanned(faces):
    while True:
        ret, frame = cap.read()
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurredFrame = cv2.blur(grayFrame, (3, 3))
        cannyFrame = cv2.Canny(blurredFrame, 30, 60, 3)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
        dilatedFrame = cv2.dilate(cannyFrame, kernel)
        contours = find_contours(dilatedFrame)
        if len(contours) == 9:
            
            frame = draw_contours(frame,contours)
            frame1 = frame
            frame1_contours = contours
            break
        image=draw_2d_cube_state(frame, faces)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    middle = frame1_contours[4]
    x = middle[0]
    y = middle[1]
    w = middle[2]
    h = middle[3]
    center_x = x + w / 2
    center_y = y + h / 2
    color = frame1[int(center_y), int(center_x)]
    middle_color = predicted_color(color)

    for idx, i in enumerate(frame1_contours):
        #get the center of the contour
        x = i[0]
        y = i[1]
        w = i[2]
        h = i[3]
        center_x = x + w / 2
        center_y = y + h / 2
        #get the color of the center of the contour
        color = frame1[int(center_y), int(center_x)]
        #draw a circle on the center of the contour
        prediction = predicted_color(color)
        faces[middle_color].update(idx,prediction)
        #write the color name on the contour
        cv2.putText(frame1, prediction, (int(center_x), int(center_y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
        cv2.circle(frame1, (int(center_x), int(center_y)), 5, (0, 0, 255), -1)
        image=draw_2d_cube_state(frame, faces)
        cv2.imshow('frame', image)
    print(faces[middle_color].get_face())


image=draw_2d_cube_state(frame, faces)
cv2.imshow('frame', image)
cv2.waitKey(0)
print("finished scan")
