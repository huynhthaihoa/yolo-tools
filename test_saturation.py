import cv2
import numpy as np
from glob import glob
import os 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="Directory contains input folder",
                    type=str, default="input")
parser.add_argument("-d", "--dif", help="Directory contains dif folder",
                    type=str, default="")
parser.add_argument("-s", "--sub", help="Directory contains sub folder",
                    type=str, default="")

args = parser.parse_args()

input = args.input
imgPaths = glob(input +"\\*.jpg")

difDir = args.dif
if difDir == "":
    difDir = input + "_dif_saturation"
if os.path.isdir(difDir) is False:
    os.mkdir(difDir)
difDir += "\\"

subDir = args.sub
if subDir == "":
    subDir = input + "_sub_saturation"
if os.path.isdir(subDir) is False:
    os.mkdir(subDir)
subDir += "\\"
prevPrefix = ""
prevImg = ""

for imgPath in imgPaths:
    prefix = os.path.basename(imgPath)
    idx1 = prefix.rfind('_')
    idx2 = prefix.rfind('.')
    prefix = prefix[idx1 + 1: idx2]
    hsvImg = cv2.imread(imgPath)#, cv2.COLOR_BGR2HSV)
    hsvImg = cv2.cvtColor(hsvImg, cv2.COLOR_BGR2HSV)
    img = hsvImg[:, :, 1]
    if prevPrefix != "":
        print("Assessing couple: {0} {1}".format(prevPrefix, prefix))
        dif = cv2.absdiff(img, prevImg)
        sub = cv2.subtract(img, prevImg)
        difImg = (dif != 0)# * 255
        subImg = (sub != 0)# * 255
        #difImg = cv2.threshold(difImg, 0, 255, cv2.THRESH_BINARY_INV)
        difPath = difDir + prevPrefix + '_' + prefix + ".png"
        subPath = subDir + prevPrefix + '_' + prefix + ".png"
        cv2.imwrite(difPath, difImg * 255)
        cv2.imwrite(subPath, subImg * 255)
    prevPrefix = prefix
    prevImg = img

print("Done!")