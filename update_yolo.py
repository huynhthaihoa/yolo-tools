"""
Update class name in YOLO annotation files based on label dataset
Created on March 5th 2021

@author: Thai-Hoa Huynh
"""
import os
from glob import glob
import cv2
import numpy as np
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Directory contains label dataset",
                    type=str, default="Labels")
    parser.add_argument("-a", "--ann", help="Directory contains YOLO annotation files",
                    type=str, default="coco/yolo")
    parser.add_argument("-c", "--class_file", help="Directory of class file",
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
    exts = ['/*.jpg', '/*.png', '/*.jpeg', '/*.jfif']
    classFile = open(args.class_file, "rt")
    classes = list()
    data = dict()
    for line in classFile:
        if line[-1] == '\n':
            classes.append(line[:-1])
        else:
            classes.append(line)
    subdirs = [x[0] for x in os.walk(args.input)]
    for subdir in subdirs:
        try:
            cls_id = classes.index(os.path.basename(subdir))
        except:
            continue
        imgs = []
        for ext in exts:
            imgs += glob(subdir + ext)
            for imgpath in imgs:
                basename = os.path.basename(imgpath)
                annname = basename[:basename.rfind('_')]
                annpath = anns + annname + '.txt'
                order = int(basename[basename.rfind('_') + 1: basename.rfind('.')])
                if os.path.isfile(annpath) is True:
                    if annpath not in data:
                        data[annpath] = np.loadtxt(annpath).reshape(-1, 5)
                    if new != '':
                        oldpath = annpath
                        annpath = new + annname + '.txt'
                        data[annpath] = data[oldpath]
                    annfile = open(annpath, "wt")
                    for i in range(len(data[annpath])):
                        data_conv = data[annpath][i]
                        if i == order:
                            data_conv[0] = cls_id
                            data[annpath][0] = cls_id
                        for j in range(5):
                            if(j == 0):
                                annfile.write(str(int(data_conv[j])))
                            else:
                                annfile.write(str(data_conv[j]))
                            if(j < 4):
                                annfile.write(' ')
                            else:
                                annfile.write('\n')
                    annfile.close()
    print('Updating YOLO annotation finished!')
