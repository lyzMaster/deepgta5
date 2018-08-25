from PIL import ImageGrab
import time
import requests
import multiprocessing
import csv


url = "https://www.pixeldesert.com/compare"
txt_position = "/Users/lyz/Desktop/state_txt.txt"

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


def main():
    global n
    with open('/Users/lyz/Desktop/data.csv', 'a', newline='') as csvfile:
        fieldnames = ['name', 'data']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        while True:
            fo = open(txt_position, "r")    #配置1
            txt = fo.read()
            fo.close()
            if txt == '0':
                print("next time begin from:"+str(n))
                print('=====================end=====================')
                break
            elif txt == '1':
                screen = ImageGrab.grab(bbox=(0, 40, 800, 640))
                writer.writerow({'name': '/Users/lyz/Desktop/rwa/gta_rgb_' + str(n) + '.jpg', 'data':[0,0,1,1,0,1,0,1]})
                screen = screen.convert('RGB')
                screen.save('/Users/lyz/Desktop/rwa/gta_rgb_' + str(n) + '.jpg')   #配置2
                n = n + 1
                print("successfully capture "+"rgb_" + str(n-1) + '.jpg')
                time.sleep(0.8)


print("Enter the index you want to begin with:")
n = int(input())
while True:
    response = requests.request("POST", url)
    if response.text[1] == '1':
        fo = open(txt_position, "w")   #配置3
        fo.write("1")
        fo.close()
        print('$$$$$$$$$$$$$$$$$$$ after 10s will begin $$$$$$$$$$$$$$$$$$$ ')
        i = 10
        while i > 0:
            print(i)
            i = i-1
            time.sleep(1)
        print('=====================start now!======================')
        break
    print("waiting for instructions...")
    time.sleep(1)

p1 = multiprocessing.Process(target=state)
p2 = multiprocessing.Process(target=main)
p1.start()
p2.start()
