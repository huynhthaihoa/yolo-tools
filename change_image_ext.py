import os
from glob import glob
import sys

input = os.path.abspath(sys.argv[1]) + '/'
imgs = glob(input + '*.jpg') + glob(input + '*.jpeg')

for img in imgs:
    pre, _ = os.path.splitext(img)
    os.rename(img, pre + '.png')
print('Finish!')