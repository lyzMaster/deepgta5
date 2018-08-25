import os

#获取指定文件夹中指定拓展名的文件名
#locate:指定的文件
#extension:指定的拓展名
#include:0,包含拓展名，1,不包含拓展名
#返回值:一个list包含文件名，默认包含拓展名
def get_filename(locate, extension, include=1):
    files = os.listdir(locate)
    filenames = []
    for file in files:
        if file.split('.')[-1] == extension:
            if include == 0:
                filenames.append(file.split('.')[0])
            elif include == 1:
                filenames.append(file)
    return filenames


