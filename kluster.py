import cv2
import numpy as np
import matplotlib.pyplot as plt
def quantimage(image,k):
    i = np.float32(image).reshape(-1,3)
    condition = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,20,1.0)
    ret,label,center = cv2.kmeans(i, k , None, condition,10,cv2.KMEANS_RANDOM_CENTERS)
    
    for x,y,z in center:
        print(f'Cluster centre: [{int(x)},{int(y)}]')
        cv2.drawMarker(image, (int(x), int(y)), [0,0,255])
    
    center = np.uint8(center)
    final_img = center[label.flatten()]
    final_img = final_img.reshape(image.shape)
    return (final_img, image)
image = cv2.imread('images/rubiks.jpg')


kmeans,image = quantimage(image,10)
colors = []
[colors.append(x) for x in kmeans.reshape(-1,3).tolist() if x not in colors]
print(colors)
blue = (255,0,0)
red = (0,0,255)
green = (0,255,0)
yellow = (0,255,255)
white = (255,255,255)

lower_red = 1000
lower_green = 1000
lower_blue = 1000
lower_yellow = 1000
lower_white = 1000

closest_blue = (0,0,0)
closest_red = (0,0,0)
closest_green = (0,0,0)
closest_yellow = (0,0,0)
closest_white = (0,0,0)
for color in colors:
    #subtract two colors
    diff_blue = np.subtract(color,blue)
    diff_red = np.subtract(color,red)
    diff_green = np.subtract(color,green)
    diff_yellow = np.subtract(color,yellow)
    diff_white = np.subtract(color,white)

    lower_blue_temp = sum([abs(x) for x in diff_blue])
    lower_red_temp = sum([abs(x) for x in diff_red])
    lower_green_temp = sum([abs(x) for x in diff_green])
    lower_yellow_temp = sum([abs(x) for x in diff_yellow])
    lower_white_temp = sum([abs(x) for x in diff_white])
    
    if lower_red_temp < lower_red:
        lower_red = lower_red_temp
        closest_red = color
    if lower_blue_temp < lower_blue:
        lower_blue = lower_blue_temp
        closest_blue = color
    if lower_green_temp < lower_green:
        lower_green = lower_green_temp
        closest_green = color
    if lower_yellow_temp < lower_yellow:
        lower_yellow = lower_yellow_temp
        closest_yellow = color
    if lower_white_temp < lower_white:
        lower_white = lower_white_temp
        closest_white = color
    
print("closest_red")
print(closest_red)
print("closest_green")
print(closest_green)
print("closest_blue")
print(closest_blue)
print("closest_yellow")
print(closest_yellow)
print("closest_white")
print(closest_white)
cv2.imshow('image',kmeans)
cv2.waitKey(0)
