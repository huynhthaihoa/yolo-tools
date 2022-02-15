import numpy as np
import albumentations as A
import random
import cv2
import argparse
import os 
from glob import glob
#from albumentations.augmentations.transforms import Posterize

def countDigit(number):
    '''
    count the number of digits of a specified number:
    @number [in]: a number to be determined
    '''
    count = 0
    while(number > 0):
        count += 1
        number = number // 10
    return count

def getSuffix(nDigits, index):
    '''
    generate image file name suffix:
    @nDigits [in]: # of digit to represent all the frames,
    @index [in]: index of the selected image
    '''
    testNum = 10
    count = 1
    while(testNum <= index):
        count += 1
        testNum *= 10
    suffix = ""
    count = nDigits - count
    #print(count)
    for i in range(count):
        suffix += "0"
    suffix += str(index)
    return suffix

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-ia", "--input_ann", help="Directory of original annotation files",
                    type=str, default="coco/yolo")
    parser.add_argument("-oa", "--output_ann", help="Directory of augmented annotation files",
                    type=str, default="coco/yolo/augmented")
    parser.add_argument("-ii", "--input_img", help="Directory of original images",
                    type=str, default="")
    parser.add_argument("-oi", "--output_img", help="Directory of augmented images",
                    type=str, default="")
    parser.add_argument("-n", "--number", help="Number of augmented images for each original images (default is 10)",
                    type=int, default=10)
    args = parser.parse_args()
    inputAnns = args.input_ann + '/'
    outputAnns = args.output_ann
    n = args.number
    nDigits = countDigit(n)
    if os.path.isdir(outputAnns) is False:
        os.mkdir(outputAnns)
    outputAnns += '/'
    inputImgs = args.input_img
    if inputImgs == "":
        inputImgs = inputAnns
    outputImgs = args.output_img
    if outputImgs == "":
        outputImgs = outputAnns
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
        if os.path.isfile(inputannpath) is True:
            lines = open(inputannpath, "rt")
            bboxes = []
            for line in lines:
                elems = line.split(' ')
                bboxes.append([float(elems[1]), float(elems[2]), float(elems[3]), float(elems[4]), int(elems[0])])
            lines.close()
            image = cv2.imread(imgpath)
            height, width, _ = image.shape
            for i in range(n):#A.ShiftScaleRotate(p=0.2)
                print(".", end="", flush=True)
                transform_list = list()
                #A.Resize()
                seed_weather = random.randint(0, 2)
                seed_contrast = random.randint(0, 2)
                seed_rotate = random.randint(0, 2)
                # seed_transpose = random.randint(0, 2)
                seed_safecrop = random.randint(0, 2)
                seed_perspective = random.randint(0, 2)
                seed_flip = random.randint(0, 2)
                seed_rgb = random.randint(0, 2)
                # if seed_weather == 0:
                #     transform_list.append(A.RandomSnow(p=0.5))
                # else:
                if seed_weather == 1:
                    transform_list.append(A.RandomRain(p=0.5))
                if seed_contrast == 1:
                    transform_list.append(A.RandomBrightnessContrast(p=0.5))
                if seed_rotate == 1:
                    transform_list.append(A.ShiftScaleRotate(p=0.5, rotate_limit=15))
                # if seed_transpose == 1:
                #     transform_list.append(A.Transpose(p=0.5))
                if seed_safecrop == 1:
                    transform_list.append(A.RandomSizedBBoxSafeCrop(height, width))
                if seed_perspective == 1:
                    transform_list.append(A.Perspective())
                if seed_flip == 1:
                    transform_list.append(A.HorizontalFlip(p=0.5))
                if seed_rgb == 1:
                    transform_list.append(A.RGBShift(r_shift_limit=30, g_shift_limit=30, b_shift_limit=30, p=0.5))
                transform = A.Compose(transforms=transform_list, bbox_params=A.BboxParams(format="yolo"))
                res = transform(image=image, bboxes=bboxes)
                outputimgpath = outputImgs + originname + '-' + getSuffix(nDigits, i) + '.png'
                outputannpath = outputAnns + originname + '-' + getSuffix(nDigits, i) + '.txt'
                cv2.imwrite(outputimgpath, res["image"])
                outfile = open(outputannpath, "wt")
                for elems in res["bboxes"]:
                    outfile.write(str(elems[4]) + ' ' + str(elems[0]) + ' ' + str(elems[1]) + ' ' + str(elems[2]) + ' ' + str(elems[3]) + '\n')
                outfile.close()
    print('Augment finished!')
