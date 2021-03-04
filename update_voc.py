import os
from glob import glob
import cv2
from xml.dom.minidom import parseString
from lxml.etree import Element, SubElement, tostring
import numpy as np
import argparse
import xml.etree.ElementTree as ET


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Directory contains new label",
                    type=str, default="Label")
    parser.add_argument("-a", "--ann", help="Directory contains annotation files",
                    type=str, default="coco/voc")
    args = parser.parse_args()
    anns = args.ann 
    anns += '/'
    exts = ['/*.jpg', '/*.png', '/*.jpeg', '/*.jfif']
    subdirs = [x[0] for x in os.walk(args.input)]
    for subdir in subdirs:
        objname = os.path.basename(subdir) 
        imgs = []
        for ext in exts:
            imgs += glob(subdir + ext)
            for imgpath in imgs:
                basename = os.path.basename(imgpath)
                annname = basename.split('_')[0]
                annpath = anns + annname + '.xml'
                order = int((basename.split('_')[1]).split('.')[0])
                if os.path.isfile(annpath) is True:
                    tree = ET.parse(annpath)
                    root = tree.getroot()
                    for j, obj in enumerate(root.iter('object')):
                        if j == order:
                            node = obj.find('name')
                            node.text = objname
                            #obj.attrib['name'] = objname
                            break
                    tree.write(annpath)
    print('Finished!')