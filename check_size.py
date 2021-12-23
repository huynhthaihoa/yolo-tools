from PIL import Image
import argparse
from glob import glob

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--img", help="Images directory", type=str, default="img")
args = parser.parse_args()

imgDir = args.img + "\\"
imgs = glob(imgDir + "*.png") + glob(imgDir + "*.jpg")
maxW = 0
maxH = 0
for imgpath in imgs:
    img = Image.open(imgpath)
    W, H = img.size
    if W > maxW:
        maxW = W
    if H > maxH:
        maxH = H
print("Max width: {0}. Max height: {1}".format(w, h))