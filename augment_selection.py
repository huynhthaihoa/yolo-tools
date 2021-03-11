import numpy as np
import albumentations as A
import random
import cv2
import argparse
import os 
from glob import glob

THRESHOLD = 1000

def getImageName(imgpath, inLabelFold=True):
    '''
    Get image name from the image path:
    @imgpath [in]: image path
    @inLabelFold [in]: image path refers image instance in label folder (True) or not (False)
    '''
    basename = os.path.basename(imgpath)
    if inLabelFold is True:
        name = basename[: basename.rfind('_')]
    else:
        name = basename.split('.')[0]
    return name

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--label", help="Directory path of label dataset",
                    type=str, default="Labels")
    parser.add_argument("-ia", "--ann", help="Directory path of original annotation files",
                    type=str, default="coco/yolo")
    parser.add_argument("-ii", "--imgs", help="Directory path of original image files",
                    type=str, default="coco/img")
    parser.add_argument("-oa", "--output_ann", help="Directory of augmented annotation files",
                    type=str, default="coco/yolo/augmented")
    parser.add_argument("-oi", "--output_imgs", help="Directory path of augmented image files",
                    type=str, default="coco/img/augmented")
    args = parser.parse_args()
    anns = args.ann 
    anns += '/'
    outputAnns = args.output_ann
    if os.path.isdir(outputAnns) is False:
        os.mkdir(outputAnns)
    outputAnns += '/'
    outputImgs = args.output_imgs
    if os.path.isdir(outputImgs) is False:
        os.mkdir(outputImgs)
    outputImgs += '/'   
    exts = ['/*.jpg', '/*.png', '/*.jpeg', '/*.jfif']
    data = dict()
    subdirs = [x[0] for x in os.walk(args.label)]
    subdirs.pop(0)
    for subdir in subdirs:
        dirname = os.path.basename(subdir)
        imgs = list()
        for ext in exts:
            imgs += glob(subdir + ext)
            for imgpath in imgs:
                if dirname not in data:
                    data[dirname] = list()
                name = getImageName(imgpath)
                if name not in data[dirname]:
                    #print('name in label folder: ', name)
                    data[dirname].append(name)
    log = open("log.txt", "wt")
    for key in data:
        #log.write(key + ':\n')
        for name in data[key]:
            log.write(name + '\n')
    log.close()
    rawimgs = list()
    for ext in exts:
        rawimgs += glob(args.imgs + ext)
    log_2 = open("log_2.txt", "wt")
    for imgpath in rawimgs:
        name = getImageName(imgpath, False)
        inputannpath = anns + name + '.txt'
        if os.path.isfile(inputannpath) is False:
            continue
        lines = open(inputannpath, "rt")
        bboxes = list()
        for line in lines:
            elems = line.split(' ')
            bboxes.append([float(elems[1]), float(elems[2]), float(elems[3]), float(elems[4]), int(elems[0])])
        size = 1
        idx = 0
        for key in data:
            if name in data[key]:
                log_2.write(name + '\n')
                #print('name in image folder: ', name)
                size = len(data[key])
                break
            idx += 1
        if idx == len(data):
            continue
        image = cv2.imread(imgpath)
        n = int(THRESHOLD / size - 1)
        if n <= 0:
            continue
        for i in range(n):#A.ShiftScaleRotate(p=0.2)
            print(".", end="", flush=True)
            transform_list = list()
            #seed_weather = random.randint(0, 2)
            #seed_contrast = random.randint(0, 2)
            #seed_rotate = random.randint(0, 2)
            seed = random.randint(0, 3)
            # if seed_weather == 0:
            #     transform_list.append(A.RandomSnow(p=0.5))
            # else:
            #     transform_list.append(A.RandomRain(p=0.5))
            #if seed_contrast == 1:
            if seed == 1 or seed == 0: 
                transform_list.append(A.RandomBrightnessContrast(p=0.5))
            #if seed_rotate == 1:
            if seed == 1 or seed == 2: 
                transform_list.append(A.ShiftScaleRotate(p=0.5, rotate_limit=15))
            transform = A.Compose(transforms=transform_list, bbox_params=A.BboxParams(format="yolo"))
            res = transform(image=image, bboxes=bboxes)
            outputimgpath = outputImgs + name + '-' + str(i) + '.jpg'
            outputannpath = outputAnns + name + '-' + str(i) + '.txt'
            cv2.imwrite(outputimgpath, res["image"])
            outfile = open(outputannpath, "wt")
            for elems in res["bboxes"]:
                outfile.write(str(elems[4]) + ' ' + str(elems[0]) + ' ' + str(elems[1]) + ' ' + str(elems[2]) + ' ' + str(elems[3]) + '\n')
            outfile.close()
    log_2.close()
    print('Augment finished!')