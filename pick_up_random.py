import os
from shutil import copyfile
from glob import glob
import argparse
import random

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input", help="Directory of input folder",
                    type=str, default="")
parser.add_argument("-o", "--output", help="Directory of output folder",
                    type=str, default="")
parser.add_argument("-n", "--num", help="Number of items to pick up",
                    type=int, default="")
args = parser.parse_args()

exts = ['.jpg', '.png', '.jfif', '.jpeg']

inpDir = args.input + '\\'
outDir = args.output
if os.path.isdir(outDir) is False:
    os.mkdir(outDir)
outDir += '/'

num = args.num

#annDir = args.ann + '\\'

imgpaths = list()

for ext in exts:
    imgpaths += glob(inpDir + '*' + ext)

data = list()

for imgpath in imgpaths:
    basename = os.path.basename(imgpath)
    annpath = inpDir + basename[: basename.rfind('.')] + '.txt'
    if os.path.exists(annpath) is True:
        data.append((basename, imgpath, annpath))

if num > len(data):
    num = len(data)

random.shuffle(data)
for i in range(num):
    basename = data[i][0]
    imgpath = data[i][1]
    annpath = data[i][2]
    imgpath_new = outDir + basename
    annpath_new = outDir + basename[: basename.rfind('.')] + '.txt'
    copyfile(imgpath, imgpath_new)
    copyfile(annpath, annpath_new)
    print(".", end="", flush=True)

print("Picking completed!")