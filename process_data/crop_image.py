from PIL import Image
import os


def image_process(file):
    image = Image.open('/Volumes/desk/image_data2/'+file)
    # croped = image.crop((0, 37, 1602, 938))     #this cut the title
    croped_top = image.crop((0, 500, 1596, 891))    #this is best
    # croped_bottom = croped_top.crop((0, 0, 1596, 380))
    croped_top.save('/Volumes/desk/croped/'+file.split('.')[0]+'.jpg')


files = os.listdir('/Volumes/desk/image_data2')
for file in files:
    if file.split('.')[-1] == 'jpg':
        image_process(file)