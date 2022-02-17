"""
Update class name in YOLO annotation files based on label dataset
Created on March 5th 2021

@author: Thai-Hoa Huynh
"""
import os
from glob import glob
#import cv2
import numpy as np
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--input", help="Directory contains label dataset",
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
    
    classes = list()
    data = dict()
    with open(args.class_file, "rt") as classFile:
        for line in classFile:
            if line[-1] == '\n':
                classes.append(line[:-1])
            #print(line[:-1] + ":" + str(len(line[:-1])))
            else:
                classes.append(line)
            #print(line + ":" + str(len(line)))
            
    subdirs = [x[0] for x in os.walk(args.input)]
    for subdir in subdirs:
        if subdir == args.input:
            continue
        #print("Oops:", classes.index(os.path.basename(subdir)))
        try:
            cls_id = classes.index(os.path.basename(subdir))
            #print('in!')
            #print(os.path.basename(subdir) + ":" + cls_id)
        except:
            cls_id = -1
            #print('not in!')
            #print(cls_id)
            #continue
        imgs = []
        for ext in exts:
            imgs += glob(subdir + ext)
            for imgpath in imgs:
                basename = os.path.basename(imgpath)
                #print(basename)
                annname = basename[:basename.rfind('_')]
                annpath = anns + annname + '.txt'
                #print(annpath)
                order = int(basename[basename.rfind('_') + 1: basename.rfind('.')])
                if os.path.isfile(annpath) is True:
                    if annpath not in data:
                        data[annpath] = np.loadtxt(annpath).reshape(-1, 5)
                    if new != '':
                        oldpath = annpath
                        annpath = new + annname + '.txt'
                        data[annpath] = data[oldpath]
                    n_bboxes = len(data[annpath])
                    for i in range(n_bboxes):
                        if i == order:
                            print(".", end="", flush=True)
                            if(int(data[annpath][i][0]) != cls_id):
                                print("*", end="", flush=True)
                                #print(str(data[annpath][i][0]) + ':' +str(cls_id))
                                #print(".", end="", flush=True)
                                data[annpath][i][0] = cls_id
                            break
    for annpath in data:
        print(",", end="", flush=True)
        annfile = open(annpath, "wt")
        n_bboxes = len(data[annpath])
        for i in range(n_bboxes):
            data_conv = data[annpath][i]
            if(int(data_conv[0]) == -1):
                continue
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
    print('\nUpdating YOLO annotation finished!')
