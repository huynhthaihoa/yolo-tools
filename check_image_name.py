import numpy as np
import albumentations as A
import random
import cv2
import argparse
import os 
from glob import glob

Hangul = {"Ah": "dk", "Ba": "qk", "Ja": "wk", "Sa": "tk"}
Region = {"Seoul": "A", "Gyeonggi": "B", "Incheon": "C", "Gangwon": "D", "Chungnam": "E", "Daejeon": "F", "Chungbuk": "G", "Busan": "H",
         "Ulsan": "I", "Daegu": "J", "Gyeongbuk": "K", "Gyeongnam": "L", "Chonnam": "M", "Gwangju": "N", "Jeonbuk": "O", "Jeju": "P",
         "Seoul vertical": "A", "Gyeonggi vertical": "B", "Incheon vertical": "C", "Gangwon vertical": "D", "Chungnam vertical": "E", "Daejeon vertical": "F", 
         "Chungbuk vertical": "G", "Busan vertical": "H", "Ulsan vertical": "I", "Daegu vertical": "J", "Gyeongbuk vertical": "K", "Gyeongnam vertical": "L", 
         "Chonnam vertical": "M", "Gwangju vertical": "N", "Jeonbuk vertical": "O", "Jeju vertical": "P"}
def extract_chars_from_index(name, idx):
    '''
    Get the characters from the image name in the specified index:
    @name [in]
    @idx [in]
    '''
    idx = int(idx)
    if(idx < 3):
        return name[idx: idx + 1]
    elif (idx == 3):
        return name[idx: idx + 2]
    return name[idx + 1: idx + 2]

def update_name_from_index(name, idx, chars):
    '''
    Update file name by chars at the specified index:
    @name [in]
    @idx [in]
    @chars [in]
    '''
    arr = list(name)
    idx = int(idx)
    if (idx <= 3):
        arr[idx] = chars[0]
    if (idx == 3):
        arr[idx + 1] = chars[1]
    elif(idx > 3):
        arr[idx + 1] = chars[0]
    return arr

def verify_label(chars, label):
    '''
    Check the characters extracted from the image name if it is compatible with the assigned label
    '''
    #chars = list(chars)
    if len(chars) == 2:
        return (chars in Hangul[label])
    #print(chars[0])
    if chars[0] >= '0' and chars[0] <= '9':
        return (chars[0] == label[0])
    #print(Region[label] + ':' + chars)
    return Region[label] == chars
    #return (chars in Region[label])

def get_name_index(filename):
    filename_without_ext = os.path.basename(filename).split('.')[0]
    name = filename_without_ext[: filename_without_ext.rfind('_')]
    index = filename_without_ext[filename_without_ext.rfind('_') + 1:]
    return name, index

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--label", help="Directory path of label dataset",
                    type=str, default="Labels")
    parser.add_argument("-a", "--ann", help="Directory path of original annotation files",
                    type=str, default="coco/yolo")
    parser.add_argument("-i", "--imgs", help="Directory path of original image files",
                    type=str, default="coco/img")
    args = parser.parse_args()
    annDir = args.ann + '/'
    imgNameDict = dict()
    extNameDict = dict()
    imgDir = args.imgs
    #annNameDict = dict()
    exts = ['/*.jpg', '/*.png', '/*.jpeg', '/*.jfif']
    imgs = list()
    for ext in exts:
        imgs += glob(imgDir + ext)
    for imgpath in imgs:
        name, ext = os.path.basename(imgpath).split('.')
        imgNameDict[name] = list(name) #os.path.basename(imgpath).split('.')[0]
        extNameDict[name] = ext
    subdirs = [x[0] for x in os.walk(args.label)]
    subdirs.pop(0)  
    log_2 = open('log_2.txt', 'wt')
    for subdir in subdirs:
        label = os.path.basename(subdir)
        imgs = glob(subdir + exts[0])
        for imgpath in imgs:
            print(".", end="", flush=True)
            log_2.write(os.path.basename(imgpath).split('.')[0] + '\n')
            name, index = get_name_index(imgpath)
            chars = extract_chars_from_index(name, index)
            log_2.write("label: " + label + '\n')
            log_2.write("name: " + name + '\n')
            log_2.write("index:" + index + '\n')
            log_2.write("char: " + chars + '\n')
            try:
                if verify_label(chars, label) is False and name in imgNameDict:
                    imgNameDict[name] = update_name_from_index(name, index, chars)
            except:
                log_2.write('Error occur!\n')
                pass
    imgDir += '/'
    log = open('log.txt', 'wt')
    for name in imgNameDict:
        if name != ''.join(imgNameDict[name]):
            log.write(name + ':' + imgNameDict[name] + '\n')
    log.close()
    log_2.close()
        # os.rename(imgDir + name + '.' + extNameDict[name], imgDir + imgNameDict[name] + '.' + extNameDict[name])
        # os.rename(annDir + name + '.txt', annDir + imgNameDict[name] + '.txt')


  
     


