from PIL import ImageGrab
import time
import requests
import multiprocessing
import csv
from getkeys import keys_to_output,key_check
from grab import grab_screen
import cv2

url = "https://www.pixeldesert.com/compare"
txt_position = "C:\\gta5_console\\state_config\\state.txt"

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
    n = 1   ###################
    with open('C:\\gta5_console\\keys_data\\keys_data.csv', 'a', newline='') as csvfile:
        fieldnames = ['position', 'data']
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
                #screen = ImageGrab.grab(bbox = (0,40,1600,938))
                screen = grab_screen(region=(0,40,1595,930))
                keydata = keys_to_output(key_check())
                screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
                cv2.imwrite('C:\\gta5_console\\image_data\\gta_rgb_' + str(n-1) + '.jpg',screen)
                #screen.save('C:\\gta5_console\\image_data\\gta_rgb_' + str(n-1) + '.jpg')   #配置2
                writer.writerow({'position': 'rgb_' + str(n-1) + '.jpg', 'data':keydata})
                n = n + 1
                print("successfully capture "+"rgb_" + str(n-1) + '.jpg')
                time.sleep(1)


if __name__ == '__main__':
	#print("Enter the index you want to begin with:")
	#n = int(input())
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
