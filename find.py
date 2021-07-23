import os
from glob import glob

annpaths = glob("*.txt")
for annpath in annpaths:
    basename = os.path.basename(annpath)
    basename = basename[:basename.rfind('.')]
    imgname = basename + '.png'
    if os.path.exists(imgname) is False:
        print(annpath)
#print('Finish!)