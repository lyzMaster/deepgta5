import cv2
import os
import numpy as np


# def image_process(file):
#     image = '/Users/lyz/Desktop/image/'+file
#     print(image)
#     image = cv2.imread(image)
#     print(image.shape)

def image_process(file):
    image = '/Users/lyz/Desktop/rgb/'+file
    print(image)
    image = cv2.imread(image)
    print(image.shape)


files = os.listdir('/Users/lyz/Desktop/rgb')
for file in files:
    if file.split('.')[-1] == 'jpg':
        image_process(file)