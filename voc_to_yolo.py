#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on March 3rd 2021

@author: Thai-Hoa Huynh
@credit: https://gist.github.com/Amir22010/a99f18ca19112bc7db0872a36a03a1ec
"""

import os
from glob import glob
import xml.etree.ElementTree as ET
import argparse

def convert(size, box):
    '''
    Convert object size into bounding box:
    @size [in]
    @box [in]
    '''
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def txt_transform(classes, inputAnn, outputAnn):  
    '''
    Convert Pascal VOC (.xml) into Yolo (.txt):
    @classes [in]:
    @inputAnn [in]:
    @outputAnn [in]:
    ''' 
    anns = glob(inputAnn + '/*.xml')
    for target in anns:
        #target = inputAnn + '/' + os.path.basename(imgpath).split('.')[0] + '.xml'
        outAnnPath = outputAnn + '/' + os.path.basename(target).split('.')[0] + '.txt'
        inFile = open(target)
        outFile = open(outAnnPath, "wt")
        tree = ET.parse(inFile)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            className = obj.find('name').text
            if className not in classes or int(difficult)==1:
                continue
            cls_id = classes.index(className)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
            bb = convert((w,h), b)
            outFile.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
        outFile.close()
        inFile.close()
       
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-y", "--output_ann", help="Directory of YOLO annotation files (.txt)",
                    type=str, default="coco/labels")
    parser.add_argument("-p", "--input_ann", help="Directory of Pascal VOC annotation files (.xml)",
                    type=str, default="coco/outputs")
    parser.add_argument("-c", "--class_file", help="Directory of class file",
                    type=str, default="obj.names")
    args = parser.parse_args()
    inputAnns = args.input_ann
    outputAnns = args.output_ann
    if os.path.isdir(outputAnns) is False:
        os.mkdir(outputAnns)
    classes = open(args.class_file, "rt")
    YOLO_CLASSES = list()
    for line in classes:
        YOLO_CLASSES.append(line[:-1])
    txt_transform(YOLO_CLASSES, inputAnns, outputAnns)
