import os
from glob import glob
import numpy as np
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--img", help="Directory of input images",
                    type=str, default="coco/images")
    parser.add_argument("-a", "--ann", help="Directory of YOLO annotation files (.txt)",
                    type=str, default="coco/yolo")
    parser.add_argument("-m", "--move", help="Directory to save redundant files",
                    type=str, default="coco/yolo")
    args = parser.parse_args()
    imgDir = args.img  + '/'
    annDir = args.ann
    mvDir = args.move 
    if os.path.isdir(mvDir) is False:
        os.mkdir(mvDir)
    mvDir += '/'
    anns = glob(annDir + '/*.txt')
    exts = ['.jpg', '.png', '.jpeg', '.jfif']
    imgs = list()
    for ext in exts:
        imgs += glob(imgDir + '*' + ext)
    for img in imgs:
        basename = os.path.basename(img)
        imgExt = basename[basename.rfind('.'):]
        basename = basename[: basename.rfind('.')]
        annpath = annDir + '/' + basename + '.txt'
        newimgpath = mvDir + basename + imgExt
        # if os.path.exists(annpath) is True:
            # print("exist: ", annpath)
        if os.path.exists(annpath) is False:
            print("redundant: ", img)
            os.rename(img, newimgpath)
            #os.remove(img)            
    for ann in anns:
        idx = 0
        for ext in exts:
            print(".", end="", flush=True)
            basename = os.path.basename(ann)
            basename = basename[: basename.rfind('.')]
            imgpath = imgDir + basename + ext
            newannpath = mvDir + basename + '.txt'
            if os.path.exists(imgpath) is True:
                #print("exist: ", imgpath)
                break
            idx += 1
        if idx == len(exts):
            print("redundant: ", annpath)
            os.rename(ann, newannpath)
            #os.remove(ann)
    print('finished!')