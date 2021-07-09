import os
from glob import glob
import random

data = list()
exts = ['.jpg', '.png', '.jfif', '.jpeg']
extLen = len(exts)
impaths = glob('img\\*.txt')
log = open("log.txt", "wt")
for impath in impaths:
    basename = os.path.basename(impath)
    basename = basename[:basename.rfind('.')]
    i = 0
    for i in range(extLen):
        fileName = 'img/' + basename + exts[i]
        if os.path.exists(fileName):
            print(fileName)
            data.append('data/' + fileName + '\n')
            break
    if i == extLen:
        #print(".", end="", flush=True)
        log.write(impath + "\n")

random.shuffle(data)

trainFile = open("train.txt", "wt")
validFile = open("valid.txt", "wt")
for line in data:
    trainFile.write(line)
    validFile.write(line)
trainFile.close()
validFile.close()
log.close()