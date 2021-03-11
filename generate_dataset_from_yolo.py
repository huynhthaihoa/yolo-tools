"""
Generate label dataset using YOLO annotation files
Created on March 4th 2021

@author: Thai-Hoa Huynh
"""

import os
from glob import glob
import cv2
import numpy as np
import argparse

def unconvert(width, height, x, y, w, h):
    '''
    Convert the normalized positions into integer positions:
    @width [in]:
    @height [in]:
    @x [in]:
    @y [in]:
    @xmin [out]:
    @xmax [out]:
    @ymin [out]:
    @ymax [out]:
    '''
    xmax = int((x*width) + (w * width)/2.0)
    xmin = int((x*width) - (w * width)/2.0)
    ymax = int((y*height) + (h * height)/2.0)
    ymin = int((y*height) - (h * height)/2.0)
    return (xmin, xmax, ymin, ymax)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--img", help="Directory of input images",
                    type=str, default="coco/images")
    parser.add_argument("-a", "--ann", help="Directory of YOLO annotation files (.txt)",
                    type=str, default="coco/yolo")
    parser.add_argument("-c", "--class_file", help="Class name file (.txt)",
                    type=str, default="obj.names")
    parser.add_argument("-o", "--output", help="Output directory to contain dataset",
                    type=str, default="Labels/")
    args = parser.parse_args()
    imgDir = args.img
    annDir = args.ann + '/'
    out = args.output
    if os.path.isdir(out) is False:
        os.mkdir(out)
    out += '/'
    classFile = open(args.class_file, "rt")
    classes = []
    for line in classFile:
        if line[-1] == '\n':
            classes.append(line[:-1])
        else:
            classes.append(line)
    exts = ['/*.jpg', '/*.png', '/*.jpeg', '/*.jfif']
    imgs = []
    for ext in exts:
        imgs += glob(imgDir + ext)
    ids = [os.path.basename(x) for x in imgs]
    for i, imgpath in enumerate(imgs):
        annpath = annDir + ids[i].split('.')[0] + '.txt'
        if os.path.isfile(annpath) is True:
            img = cv2.imread(imgpath)
            height, width, _ = img.shape
            inFile = open(annpath, "rt")
            for j, line in enumerate(inFile):
                elems = line.split(' ')
                try:
                    className = classes[int(elems[0])]
                except:
                    className = 'outlier'
                classDir = out + className
                if os.path.isdir(classDir) is False:
                    os.mkdir(classDir)
                classDir += '/'
                (xmin, xmax, ymin, ymax) = unconvert(width, height, float(elems[1]), float(elems[2]), float(elems[3]), float(elems[4]))
                cropImg = img[ymin : ymax, xmin : xmax]
                try:
                    print(".", end="", flush=True)
                    cv2.imwrite(classDir + ids[i].split('.')[0] + '_' + str(j) + '.jpg', cropImg)
                except:
                    pass
            inFile.close()
    print('Generating dataset from YOLO annotation finished!')