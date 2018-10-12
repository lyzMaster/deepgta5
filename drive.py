import time
import requests
import multiprocessing

import numpy as np
from keras.models import load_model

from img_process import process
from gamepad import AXIS_MIN, AXIS_MAX, TRIGGER_MAX, XInputDevice

from lane_detection import detect_lane

gamepad = None

url = "https://www.pixeldesert.com/compare"
txt_position = "state_config/state.txt"


def state():
    while True:
        response = requests.request("POST", url)
        fo = open(txt_position, "w")
        if response.text[1] == '0':
            fo.write("0")
        elif response.text[1] == '1':
            fo.write("1")
        fo.close()
        time.sleep(2)


def set_gamepad(control, throttle):

    trigger = int(round(throttle * TRIGGER_MAX))

    if trigger >= 0:           # control speed, L==back, R==go
        gamepad.SetTrigger('L', 0)
        gamepad.SetTrigger('R', trigger)
    else:
        trigger = -trigger
        gamepad.SetTrigger('L', trigger)
        gamepad.SetTrigger('R', 0)

    if control == -1:         # stop the car
        gamepad.SetTrigger('R', 0)
        gamepad.SetTrigger('L', 200)
        return

    if control >= 0:      # control direction
        axis = int(round(control * AXIS_MAX*1.3))
    else:
        axis = int(round(control * (-AXIS_MIN*1.3)))
    gamepad.SetAxis('X', axis)


def drive(model):
    throttle = 0
    left_line_max = 75
    right_line_max = 670

    screen, roi, radar, speed = process("Grand Theft Auto V")

    controls = model.predict([np.array([roi]), np.array([radar]), np.array([speed])], batch_size=1)

    if controls > 0:
        print("-->" + "   speed=" + str(speed))
    else:
        print("<--" + "   speed=" + str(speed))

    if speed < 19:       # control speed
        throttle = 0.6
    elif speed < 45:
        throttle = 0.4
    elif speed > 50:
        throttle = 0.0

    lane = detect_lane(screen)

    if lane[0] and lane[0][0] > left_line_max:
        if abs(controls[0][0]) < 0.27:
            controls[0][0] = 0.27
    elif lane[1] and lane[1][0] < right_line_max:
        if abs(controls[0][0]) < 0.27:
            controls[0][0] = -0.27

    return controls[0][0], throttle


def main():
    # load model
    model = load_model("models/main_model.h5")
    global gamepad
    gamepad = XInputDevice(1)
    gamepad.PlugIn()
    while True:
        fo = open(txt_position, "r")  # 配置1
        txt = fo.read()
        fo.close()
        if txt == '0':
            set_gamepad(-1,-1)
            time.sleep(0.7)
            gamepad.UnPlug()
            print('=====================end=====================')
            break
        elif txt == '1':
            control, throttle = drive(model)
            set_gamepad(control, throttle)


if __name__ == '__main__':
    while True:
        response = requests.request("POST", url)
        if response.text[1] == '1':
            fo = open(txt_position, "w")
            fo.write("1")
            fo.close()
            print('$$$$$$$$$$$$$$$$$$$ after 3s will begin $$$$$$$$$$$$$$$$$$$')
            i = 3
            while i > 0:
                print(i)
                i = i - 1
                time.sleep(1)
            print('=====================start now!======================')
            break
        print("waiting for instructions...")
        time.sleep(1)

    p1 = multiprocessing.Process(target=state)
    p2 = multiprocessing.Process(target=main)
    p1.start()
    p2.start()
