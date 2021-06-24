import os
from glob import glob
import random

data = list()
exts = ['.jpg', '.png', '.jfif', '.jpeg']
extLen = len(exts)
impaths = glob('img\\*.txt')
for impath in impaths:
    basename = os.path.basename(impath)
    basename = basename[:basename.rfind('.')]
    for ext in exts:
        fileName = 'img/' + basename + ext
        if os.path.exists(fileName):
            #print(fileName)
            data.append('data/' + fileName + '\n')
            break
random.shuffle(data)
trainFile = open("train.txt", "wt")
validFile = open("valid.txt", "wt")
for line in data:
    trainFile.write(line)
    validFile.write(line)
trainFile.close()
validFile.close()