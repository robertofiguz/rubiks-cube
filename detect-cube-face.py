import cv2
import sys
import numpy as np

def main():
    video = cv2.VideoCapture(0)
    is_ok, bgr_image_input = video.read()
    

    if not is_ok:
        print("Cannot read video source")
        sys.exit()

    h1 = bgr_image_input.shape[0]
    w1 = bgr_image_input.shape[1]
    
    while True:
        _, camera = video.read()

        gray = cv2.cvtColor(camera,cv2.COLOR_BGR2GRAY)

        binary = cv2.adaptiveThreshold(gray,20,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,5,0)



        try:
         _, contours, hierarchy = cv2.findContours(binary,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE)
        except:
            contours, hierarchy = cv2.findContours(binary,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE)

        for contour in contours:
            area = cv2.contourArea(contour)
            if not (area < 3000 and area > 1000):
                continue
            perimeter = cv2.arcLength(contour, True)
            epsilon = 0.01 * perimeter
            approx = cv2.approxPolyDP(contour, epsilon, True)
            hull = cv2.convexHull(contour)
            x, y, w, h = cv2.boundingRect(contour)

            cv2.drawContours(camera,[contour],0,(255, 255, 0),2)
            cv2.drawContours(camera, [approx], 0, (255, 255, 0), 2)

        cv2.imshow("camera", camera)
        cv2.imshow("binary", binary)

        key_pressed = cv2.waitKey(1) & 0xFF
        if key_pressed == 27 or key_pressed == ord('q'):
            break


if __name__ == "__main__":
    main()