"""
Update class name in VOC annotation files based on label dataset
Created on March 4th 2021

@author: Thai-Hoa Huynh
"""

import os
from shutil import copy
from glob import glob
import cv2
import numpy as np
import argparse
import xml.etree.ElementTree as ET

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Directory contains label dataset",
                    type=str, default="Label")
    parser.add_argument("-a", "--ann", help="Directory contains Pascal VOC annotation files",
                    type=str, default="coco/voc")
    parser.add_argument("-c", "--class_file", help="Directory of class file (for checking class existence)",
                    type=str, default="obj.names")
    parser.add_argument("-n", "--new", help="Directory contains new annotation files (if user wants to save updates on new files)",
                    type=str, default="")
    args = parser.parse_args()
    anns = args.ann 
    anns += '/'
    new = args.new
    if new != "":
        if os.path.isdir(new) is False:
            os.mkdir(new)
        new += '/'
    classFile = open(args.class_file, "rt")
    classes = list()
    for line in classFile:
        if line[-1] == '\n':
            classes.append(line[:-1])
        else:
            classes.append(line)
    exts = ['/*.jpg', '/*.png', '/*.jpeg', '/*.jfif']
    subdirs = [x[0] for x in os.walk(args.input)]
    for subdir in subdirs:
        classname = os.path.basename(subdir) 
        if classname not in classes:
            continue
        imgs = []
        for ext in exts:
            imgs += glob(subdir + ext)
            for imgpath in imgs:
                basename = os.path.basename(imgpath)
                annname = basename[:basename.rfind('_')]
                annpath = anns + annname + '.xml'
                order = int(basename[basename.rfind('_') + 1: basename.rfind('.')])
                if os.path.isfile(annpath) is True:
                    if new != "":
                        newpath = new + annname + '.xml'
                        annpath = copy(annpath, newpath)
                    tree = ET.parse(annpath)
                    root = tree.getroot()
                    for j, obj in enumerate(root.iter('object')):
                        if j == order:
                            node = obj.find('name')
                            node.text = classname
                            break
                    tree.write(annpath)
    print('Updating Pascal VOC annotation finished!')