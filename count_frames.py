import cv2
import argparse
import os 
from glob import glob
from distutils.util import strtobool

def getFrameNum(videoname):
    '''
    get the number of frames in video:
    @nvideoname [in]: path of video
    '''
    source = cv2.VideoCapture(videoname)
    count = 0
    while True:
        ret, _ = source.read()
        if not ret:
            break
        count += 1
    source.release()
    return count

def countDigit(nFrames):
    '''
    count the number of digits of a specified number:
    @nFrames [in]: a number to be determined
    '''
    count = 0
    while(nFrames > 0):
        count += 1
        nFrames = nFrames // 10
    return count

def getSuffix(nDigits, index):
    '''
    generate image file name suffix:
    @nDigits [in]: # of digit to represent all the frames,
    @index [in]: index of the selected image
    '''
    testNum = 10
    count = 1
    while(testNum <= index):
        count += 1
        testNum *= 10
    suffix = ""
    count = nDigits - count
    #print(count)
    for i in range(count):
        suffix += "0"
    suffix += str(index)
    return suffix

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Path to the input folder",
                    type=str, default="")

    args = parser.parse_args()
    
    inp = args.input
    if inp != "":
        inp += '/'

    inputPaths = glob(inp + '*.mp4') + glob(inp + '*.h264') + glob(inp + '*.avi')
    txtPath = inp + "report.txt"
    txtFile = open(txtPath, "wt")
    for inputPath in inputPaths:
        print(inputPath)
        source = cv2.VideoCapture(inputPath)
        nFrames = getFrameNum(inputPath)
        a = "{0} has {1} frames\n".format(inputPath, nFrames)
        print(a)
        txtFile.write(a)
    
    txtFile.close()
        #print("{0} has {1} frames", inputPath, nFrames)
        # nDigits = countDigit(nFrames)
        # print("# of digits:", nDigits)