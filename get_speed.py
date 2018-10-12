import cv2
import time
import os
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.externals import joblib
import grab


# pre data processing:Collect GTA5 game images. Resolution of GTA5 is 800*600
def get_speed_img():
    a = 73
    time.sleep(5)
    while True:
        screen = grab.screen("Grand Theft Auto V")
        cv2.imwrite("middle_material/speed_module/data_speed/"+str(a)+".jpg", screen)
        a = a+1
        time.sleep(1)


# pre data processing:Cut out the bottom right corner speed pixels
def cut_speed_down():
    for img_name in os.listdir("middle_material/speed_module/data_speed"):
        img = cv2.imread("middle_material/speed_module/data_speed/"+img_name)
        speed = img[564:589, 747:800]
        cv2.imwrite("middle_material/speed_module/raw_speed/"+img_name, speed)


# pre data processing:convert GBR photos to binary photos
def convert2binary():
    for img_name in os.listdir("middle_material/speed_module/raw_speed"):
        img = cv2.imread("middle_material/speed_module/raw_speed/" + img_name)
        gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        ret, bin = cv2.threshold(gray_img, 200, 255, cv2.THRESH_BINARY_INV)
        cv2.imwrite("middle_material/speed_module/binary_speed/" + img_name, bin)


# pre data processing:Crop the digital pixels in each image as separate images
def cut_num_out():
    for img_name in os.listdir("middle_material/speed_module/raw_speed"):
        img = cv2.imread("middle_material/speed_module/raw_speed/" + img_name)
        img_num = img_name.split('.')[0]
        gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        ret, bin = cv2.threshold(gray_img, 200, 255, cv2.THRESH_BINARY_INV)

        bin, contours, hierarchy = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for i in range(len(contours)):
            a = cv2.minAreaRect(contours[i])
            a = cv2.boxPoints(a)
            top_x = int(a[1][0])
            top_y = int(a[1][1])
            bottom_x = int(a[3][0])
            bottom_y = int(a[3][1])
            if top_y > bottom_y:
                tmp = bottom_y
                bottom_y = top_y
                top_y = tmp
            if top_x > bottom_x:
                tmp = bottom_x
                bottom_x = top_x
                top_x = tmp
            img1 = bin[top_y:bottom_y, top_x:bottom_x]
            cv2.imwrite("middle_material/speed_module/digit/"+img_num+'_'+str(i)+'.jpg', img1)
    print("done")


# pre data processing:Test individual image digital cropping effects
def cut_pre_pic_num_out():
    a = 77
    img = cv2.imread("middle_material/speed_module/raw_speed/" + str(a) + ".jpg")
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, bin = cv2.threshold(gray_img, 200, 255, cv2.THRESH_BINARY_INV)

    bin, contours, hierarchy = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    points = []
    for i in range(len(contours)):
        a = cv2.minAreaRect(contours[i])
        a = cv2.boxPoints(a)
        top_x = int(a[1][0])
        top_y = int(a[1][1])
        bottom_x = int(a[3][0])
        bottom_y = int(a[3][1])
        if top_y > bottom_y:   # Arrange the boundary points of the recognized numbers correctly
            tmp = bottom_y
            bottom_y = top_y
            top_y = tmp
        if top_x > bottom_x:
            tmp = bottom_x
            bottom_x = top_x
            top_x = tmp
        points.append([top_y, bottom_y, top_x, bottom_x])  # Store digits' borders as a list
        if i > 0:                           # Sort recognized digits' borders from right to left
            if points[i-1][2] < top_x:
                tmp = points[i]
                points[i] = points[i-1]
                points[i-1] = tmp

    print(len(contours))
    print(bin.shape)

    img1 = bin[points[1][0]:points[1][1], points[1][2]:points[1][3]]    # 第几维度表示第几位数字，从右向左，最右为0
    # cv2.rectangle(img, (top_x, top_y), (bottom_x, bottom_y), (0, 0, 0))
    print(points[0])

    cv2.imshow("ASA", img1)
    cv2.waitKey(0)
    print("done")


# pre data processing:Classify 0～9 the ten digits and store it as an 'npy' file
def img_resize():
    sample = []
    lables = []
    for i in range(9):
        for img_name in os.listdir("middle_material/speed_module/dig/"+str(i)):
            gray_img = cv2.imread("middle_material/speed_module/dig/" + str(i) + "/" + img_name, cv2.IMREAD_GRAYSCALE)
            ret, img = cv2.threshold(gray_img, 200, 255, cv2.THRESH_BINARY)
            res = cv2.resize(img, (100, 1))   # resize photo as 100*1 matrix
            print(res)
            res = np.array(res)
            res = res.reshape(-1)    # resize the 100*1 matrix to 100 vector.Because sklearn.fit does not support 3-dims data
            sample.append(res)
            lables.append(i)
            print(i)
    samples = np.array(sample)
    labels = np.array(lables)
    labels = labels.reshape((labels.size, ))
    np.save("middle_material/speed_module/sample2.npy", samples)
    np.save("middle_material/speed_module/label2.npy", labels)


# pre data processing:Display npy file
def print_npy():
    sample = np.load("middle_material/speed_module/sample.npy")
    label = np.load("middle_material/speed_module/label2.npy")

    print(sample.shape)

    print(sample[20])
    print(label[20])


# final:Convert RGB raw multi-digital images into matrices
def process_img(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, bin = cv2.threshold(gray_img, 200, 255, cv2.THRESH_BINARY_INV)

    bin, contours, hierarchy = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    points = []
    X = []
    for i in range(len(contours)):
        a = cv2.minAreaRect(contours[i])
        a = cv2.boxPoints(a)
        top_x = int(a[1][0])
        top_y = int(a[1][1])
        bottom_x = int(a[3][0])
        bottom_y = int(a[3][1])
        if top_y > bottom_y:
            tmp = bottom_y
            bottom_y = top_y
            top_y = tmp
        if top_x > bottom_x:
            tmp = bottom_x
            bottom_x = top_x
            top_x = tmp
        points.append([top_y, bottom_y, top_x, bottom_x])
        if i > 0:  # 使存储的边界的数字，是从右向左排列
            if points[i - 1][2] < top_x:
                tmp = points[i]
                points[i] = points[i - 1]
                points[i - 1] = tmp

    for i in range(len(contours)):
        top_y = int(points[i][0])
        bottom_y = int(points[i][1])
        top_x = int(points[i][2])
        bottom_x = int(points[i][3])
        digit = bin[top_y:bottom_y, top_x:bottom_x]
        digit = cv2.resize(digit, (100, 1))
        #print(digit)
        digit = np.array(digit)
        digit = digit.reshape(-1)     # cause sklearn.fit just support <3 dims ,reshape data from 3 dims to 2
        X.append(digit)

    X = np.array(X)

    return X


# pre:train and save the speed model using KNN
def train_and_save_model():
    X = np.load("middle_material/speed_module/sample2.npy")
    y = np.load("middle_material/speed_module/label2.npy")
    neigh = KNeighborsClassifier(n_neighbors=3)
    neigh.fit(X, y)
    joblib.dump(neigh, "speed_model/speed_recognition2.pkl")


# pre:test to predict a single image
def speed_predict():
    img_pre = cv2.imread("middle_material/speed_module/raw_speed/78.jpg")
    x_pre = process_img(img_pre)

    clf = joblib.load("speed_model/speed_recognition2.pkl")
    a = clf.predict(x_pre)
    print(a)

