import osdesert
import imgdesert
import cv2

for file in osdesert.get_filename('/Users/lyz/Desktop/rgbc/', 'jpg'):
    image = imgdesert.auto_canny('/Users/lyz/Desktop/rgbc/'+file)
    cv2.imwrite("/Users/lyz/Desktop/cannyed/"+file, image)
