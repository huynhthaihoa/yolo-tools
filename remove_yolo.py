import os
from glob import glob
import cv2
import numpy as np
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--img", help="Directory of input images",
                    type=str, default="coco/images")
    parser.add_argument("-a", "--ann", help="Directory of YOLO annotation files (.txt)",
                    type=str, default="coco/yolo")
    args = parser.parse_args()
    imgDir = args.img  + '/'
    annDir = args.ann
    anns = glob(annDir + '/*.txt')
    exts = ['.jpg', '.png', '.jpeg', '.jfif', '.JPG']
    imgs = list()
    for ext in exts:
        imgs += glob(imgDir + '*' + ext)
    for img in imgs:
        annpath = annDir + '/' + os.path.basename(img).split('.')[0] + ext
        if os.path.exists(annpath) is True:
            print("exist: ", annpath)
        else:
            print("redundant: ", img)
            os.remove(img)            
    for ann in anns:
        idx = 0
        for ext in exts:
            print(".", end="", flush=True)
            imgpath = imgDir + os.path.basename(ann).split('.')[0] + ext
            if os.path.exists(imgpath) is True:
                print("exist: ", imgpath)
                break
            idx += 1
        if idx == len(exts):
            print("redundant: ", annpath)
            os.remove(ann)
    print('Finished!')