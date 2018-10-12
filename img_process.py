import cv2
from get_speed import process_img
from sklearn.externals import joblib
import grab

IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS = 66, 200, 3


def predict(img, knn):
    ret, result, neighbours, dist = knn.findNearest(img, k=1)
    return result


speed_rec = joblib.load("speed_model/speed_recognition2.pkl")  # load speed recognition KNN model


# convert speed image to int
def convert_speed(img):
    img = process_img(img)
    digits = speed_rec.predict(img)
    ten = 1
    sum = 0
    for i in range(len(digits)):
        sum += ten*digits[i]
        ten = ten*10
    return sum


def crop(image):
    return image[90:-50, :, :]   # get roi


def resize(image):
    return cv2.resize(image, (IMAGE_WIDTH, IMAGE_HEIGHT), cv2.INTER_AREA)   # resize to fit the NN


def rgb2yuv(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2YUV)


def process(winName:str = "Grand Theft Auto V"):
    screen = grab.screen(winName)
    raw_speed = screen[564:589, 747:800]
    speed = convert_speed(raw_speed)
    resized = cv2.resize(screen, (320, 240))
    radar = cv2.cvtColor(resized[212:232, 22:42, :], cv2.COLOR_RGB2BGR)[:, :, 2:3]

    roi = resized[90:-50, :, :]
    roi = cv2.resize(roi, (IMAGE_WIDTH, IMAGE_HEIGHT), cv2.INTER_AREA)
    roi_yuv = cv2.cvtColor(roi, cv2.COLOR_BGR2YUV)

    return screen, roi_yuv, radar, speed

#
# while True:
#     screen = grab.screen("Grand Theft Auto V")
#     raw_speed = screen[564:589, 747:800]
#     speed = convert_speed(raw_speed)
#     cv2.imshow("asd", raw_speed)
#     print(speed)
#     cv2.waitKey(1)