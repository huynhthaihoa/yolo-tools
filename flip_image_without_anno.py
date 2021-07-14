import numpy as np
import albumentations as A
import random
import cv2
import argparse
import os 
from glob import glob
#from albumentations.augmentations.transforms import Posterize

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", help="Directory of original images",
                    type=str, default="img")
    parser.add_argument("-o", "--output", help="Directory of flipped images",
                    type=str, default="flip")
    # parser.add_argument("-n", "--number", help="Number of augmented images for each original images (default is 10)",
    #                 type=int, default=10)
    args = parser.parse_args()
    inputImgs = args.input
    outputImgs = args.output
    if os.path.isdir(outputImgs) is False:
        os.mkdir(outputImgs)
    outputImgs += '/'
    imgs = list()
    exts = ['/*.jpg', '/*.png', '/*.jpeg', '/*.jfif']
    for ext in exts:
        imgs += glob(inputImgs + ext)
    for imgpath in imgs:
        basename = os.path.basename(imgpath)
        #originname = basename.split('.')[0]
        outputimgpath = outputImgs + basename
        #if os.path.isfile(inputannpath) is True:
        image = cv2.imread(imgpath)
        #print(imgpath)
        print(".", end="", flush=True)
        transform_list = list()
        transform_list.append(A.VerticalFlip(p=1))
        transform_list.append(A.HorizontalFlip(p=1))
        transform = A.Compose(transforms=transform_list)#, bbox_params=A.BboxParams(format="yolo"))
        res = transform(image=image)
        res = transform(image=image)
        cv2.imwrite(outputimgpath, res["image"])
        #outfile.close()
    print('Augment finished!')
