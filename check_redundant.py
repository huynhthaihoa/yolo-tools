import os
from glob import glob
import argparse


parser = argparse.ArgumentParser()

parser.add_argument("-i", "--img", help="Directory of input images",
                    type=str, default="")
parser.add_argument("-a", "--ann", help="Directory of YOLO annotation files (.txt)",
                    type=str, default="")
args = parser.parse_args()

exts = ['.jpg', '.png', '.jfif', '.jpeg']
exts_size = len(exts)
log = open("redundant.txt", "wt")
extLen = len(exts)

imgDir = args.img + '\\'
annDir = args.ann + '\\'

imgpaths = list()

for ext in exts:
    imgpaths += glob(imgDir + '*' + ext)
    
for imgpath in imgpaths:
    basename = os.path.basename(imgpath)
    fileName = annDir + basename[: basename.rfind('.')] + '.txt'
    if os.path.exists(fileName) is False:
        print("Redundant image file: ", imgpath)
        log.write(imgpath)
        log.write('\n')


annpaths = glob(annDir + '*.txt')
for annpath in annpaths:
    basename = os.path.basename(annpath)
    basename = basename[: basename.rfind('.')]
    i = 0
    for i in range(exts_size):
        fileName = imgDir + basename + exts[i]
        if os.path.exists(fileName):
            break
    if i == exts_size:
        print("Redundant annotation file: ", annpath)
        log.write(annpath)
        log.write("\n")

log.close()