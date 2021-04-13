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

    parser.add_argument("-ia", "--input_ann", help="Directory of original annotation files",
                    type=str, default="coco/yolo")
    parser.add_argument("-ii", "--input_img", help="Directory of original images",
                    type=str, default="coco/images")
    parser.add_argument("-oa", "--output_ann", help="Directory of flipped annotation files",
                    type=str, default="coco/yolo/augmented")
    parser.add_argument("-oi", "--output_img", help="Directory of flipped images",
                    type=str, default="coco/images/augmented")
    # parser.add_argument("-n", "--number", help="Number of augmented images for each original images (default is 10)",
    #                 type=int, default=10)
    args = parser.parse_args()
    inputAnns = args.input_ann + '/'
    outputAnns = args.output_ann
    #n = args.number
    if os.path.isdir(outputAnns) is False:
        os.mkdir(outputAnns)
    outputAnns += '/'
    inputImgs = args.input_img
    outputImgs = args.output_img
    if os.path.isdir(outputImgs) is False:
        os.mkdir(outputImgs)
    outputImgs += '/'
    imgs = list()
    exts = ['/*.jpg', '/*.png', '/*.jpeg', '/*.jfif']
    for ext in exts:
        imgs += glob(inputImgs + ext)
    for imgpath in imgs:
        basename = os.path.basename(imgpath)
        originname = basename.split('.')[0]
        inputannpath = inputAnns + originname + '.txt'
        outputannpath = outputAnns + originname + '.txt'
        outputimgpath = outputImgs + originname + '.jpg'
        if os.path.isfile(inputannpath) is True:
            infile = open(inputannpath, "rt")
            outfile = open(outputannpath, "wt")
            bboxes = []
            for line in infile:
                elems = line.split(' ')
                outfile.write(elems[0] + ' ' + str(1 - float(elems[1])) + ' ' + str(1 - float(elems[2])) + ' ' + elems[3] + ' ' + elems[4])
            outfile.close()
            infile.close()
            image = cv2.imread(imgpath)
            print(imgpath)
            print(".", end="", flush=True)
            transform_list = list()
            transform_list.append(A.VerticalFlip(p=1))
            transform_list.append(A.HorizontalFlip(p=1))
            transform = A.Compose(transforms=transform_list)#, bbox_params=A.BboxParams(format="yolo"))
            res = transform(image=image, bboxes=bboxes)
            cv2.imwrite(outputimgpath, res["image"])
            outfile.close()
    print('Augment finished!')
