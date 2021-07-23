import os
import sys
#import numpy as np
from glob import glob
from shutil import copyfile

#imgs = glob('*.png') + glob('*.jpg') + glob('*.jpeg')
origin = os.path.abspath(sys.argv[1])
filenames = glob('*.txt')
with open(origin, 'r') as file:
    data = file.read()
#data = np.loadtxt(origin)#.reshape(-1, 5)
for filename in filenames:
    print(filename)
    if filename == origin:
        continue
    anno = open(filename, "at")
    anno.write(data)
    anno.close()
print('Finish!')
    