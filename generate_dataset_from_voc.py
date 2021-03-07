"""
Generate label dataset using Pascal VOC annotation files
Created on March 4th 2021

@author: Thai-Hoa Huynh
"""

import os
from glob import glob
import cv2
import xml.etree.ElementTree as ET
import numpy as np
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--img", help="Directory of input images",
                    type=str, default="coco/images")
    parser.add_argument("-a", "--ann", help="Directory of VOC Pascal annotation files (.xml)",
                    type=str, default="coco/voc")
    parser.add_argument("-o", "--output", help="Output directory to contain dataset",
                    type=str, default="Label/")
    args = parser.parse_args()
    imgDir = args.img
    anns = args.ann + '/'
    out = args.output
    if os.path.isdir(out) is False:
        os.mkdir(out)
    out += '/'
    exts = ['/*.jpg', '/*.png', '/*.jpeg', '/*.jfif']
    imgs = list()
    for ext in exts:
        imgs += glob(imgDir + ext)
    ids = [os.path.basename(x) for x in imgs]
    for i, imgpath in enumerate(imgs):
        annpath = anns + ids[i].split('.')[0] + '.xml'
        if os.path.isfile(annpath) is True:
            print(annpath)
            img = cv2.imread(imgpath)
            inFile = open(annpath)
            tree = ET.parse(inFile)
            root = tree.getroot()
            for j, obj in enumerate(root.iter('object')):
                className = obj.find('name').text
                classDir = out + className
                if os.path.isdir(classDir) is False:
                    os.mkdir(classDir)
                classDir += '/'
                xmlbox = obj.find('bndbox')
                cropImg = img[int(xmlbox.find('ymin').text): int(xmlbox.find('ymax').text), int(xmlbox.find('xmin').text): int(xmlbox.find('xmax').text)]
                try:
                    cv2.imwrite(classDir + ids[i].split('.')[0] + '_' + str(j) + '.jpg', cropImg)
                except:
                    pass
            inFile.close()
    print('Generating dataset from Pascal VOC annotation finished!')