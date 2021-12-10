from glob import glob
import os
import argparse

def getSuffix(imgname):
    '''
    Get the number suffix from the image name
    '''
    numStr = imgname.split('_')[-1]
    numStr = numStr.split('.')[0]
    return int(numStr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Directory contains images",
                    type=str, default="D:\img_detection")                               
    parser.add_argument("-s", "--step", help="Distance between 2 adjacent saved frames (default is 1)", 
                    type=int, default=1)
    args = parser.parse_args()

    inp = args.input
    if inp != "":
        inp += '\\'
    step = args.step

    imgs = glob(inp + '*.png')

    for img in imgs:
        num = getSuffix(img)
        if num % step != 0:
            os.remove(img)
            print(".", end="", flush=True)
    
    print("Remove frames finished!")

