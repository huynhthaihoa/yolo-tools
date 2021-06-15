import os
import sys
from glob import glob
from shutil import copyfile

imgs = glob('*.png') + glob('*.jpg') + glob('*.jpeg')
origin = os.path.abspath(sys.argv[1])
print(origin)
for img in imgs:
    print(img)
    abspath = os.path.abspath(img)
    name = abspath[:abspath.rfind('.')] + '.txt'
    #name = os.path.abspath(img).split('.')[0] + '.txt'
    print(name)
    #name = os.path.basename(img).split('.')[0] + '.txt'
    copyfile(origin, name)
print('Finish!')
    