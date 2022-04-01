import cv2 as cv
import argparse
import os
from glob import glob
import numpy as np

def convert(width, height, x, y, w, h):
    '''
    Convert the normalized positions into integer positions:
    ###
    @width [in]: image width
    @height [in]: image height
    @x [in]: x value (2nd value) in one annotation line 
    @y [in]: y value (3rd value) in one annotation line 
    @w [in]: w value (4th value) in one annotation line
    @h [in]: h value (5th value) in one annotation line
    ###
    @xmin [out]: x min
    @xmax [out]: x max
    @ymin [out]: y min
    @ymax [out]: y max
    '''
    xmax = int((x*width) + (w * width)/2.0)
    xmin = int((x*width) - (w * width)/2.0)
    ymax = int((y*height) + (h * height)/2.0)
    ymin = int((y*height) - (h * height)/2.0)
    return xmin, xmax, ymin, ymax

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--img", help="Directory of input images",
                    type=str, default="img")
    parser.add_argument("-a", "--ann", help="Directory of annotation files (.txt)",
                    type=str, default="")
    parser.add_argument("-m", "--mask", help="Directory of masks",
                    type=str, default="mask")
    
    args = parser.parse_args()
    imgDir = args.img 
    annDir = args.ann
    if annDir == "":
        annDir = imgDir
    annDir += "\\"
    maskDir = args.mask
    if os.path.isdir(maskDir) is False:
        os.mkdir(maskDir)
    maskDir += "\\"
        
    imgPaths = glob(imgDir + "\\*.jpg") + glob(imgDir + "\\*.png")
    for imgPath in imgPaths:
        img = cv.imread(imgPath, 0)
        height, width = img.shape
        mask = np.zeros((height, width))
        imgName = os.path.basename(imgPath)
        name = imgName.split('.')[0]
        print(name)
        annPath = annDir + name + ".txt"
        annData = np.loadtxt(annPath).reshape(-1, 5)
        for idx in range(len(annData)):
            annLine = annData[idx]
            xmin, xmax, ymin, ymax = convert(width, height, annLine[1], annLine[2], annLine[3], annLine[4])
            print("{0} {1} {2} {3}".format(xmin, xmax, ymin, ymax))
            for i in range(xmin, xmax):
                for j in range(ymin, ymax):
                    mask[j][i] = 255
        maskPath = maskDir + name.split('_')[0] + ".png"
        cv.imwrite(maskPath, mask)
    print("Done!")
        