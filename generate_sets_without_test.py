import os
from glob import glob
import random

data = list()
exts = ['.jpg', '.png', '.jfif', '.jpeg']
extLen = len(exts)
impaths = glob('img\\*.txt')
log = open("log_generate.txt", "wt")
lines = list()
for line in log:
    lines.append(os.path.basename(line).split('.')[0])
log.close()
for impath in impaths:
    basename = os.path.basename(impath).split('.')[0]
    if basename in lines:
        print('Not exist: ' + basename)
        continue
    idx = 0
    for ext in exts:
        fileName = 'img/' + basename + ext
        if os.path.exists(fileName):
            #print(fileName)
            data.append('data/' + fileName + '\n')
            break
        else:
            idx += 1
    if idx == extLen:
        print(basename)
print(len(data))
random.shuffle(data)
trainFile = open("train.txt", "wt")
validFile = open("valid.txt", "wt")
for line in data:
    trainFile.write(line)
    validFile.write(line)
trainFile.close()
validFile.close()