import cv2
import argparse
import os 
from glob import glob

def getFrameNum(videoname):
    source = cv2.VideoCapture(videoname)
    count = 0
    while True:
        ret, _ = source.read()
        if not ret:
            break
        count += 1
    return count

def countDigit(nFrames):
    count = 0
    while(nFrames > 0):
        count += 1
        nFrames = nFrames // 10
    return count

def getSuffix(nDigits, index):
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
    parser.add_argument("-o", "--output", help="Path to the output folder",
                    type=str, default="output")
    parser.add_argument("-e", "--entry", help="The first index of the image (default is 0)", 
                    type=int, default=0)
    parser.add_argument("-f", "--frequency", help="Frequency (distance between 2 adjacent saved frames - default is 1)", 
                    type=int, default=1)
    args = parser.parse_args()
    out = args.output
    entryIdx = args.entry
    freq = args.frequency
    if os.path.isdir(out) is False:
        os.mkdir(out)
    out += '/'
    
    inp = args.input
    if inp != "":
        inp += '/'

    inputPaths = glob(inp + '*.mp4') + glob(inp + '*.h264')

    for inputPath in inputPaths:
        source = cv2.VideoCapture(inputPath)
        nFrames = getFrameNum(inputPath)
        print("Frames:", nFrames)
        nDigits = countDigit(nFrames)
        print("# of digits:", nDigits)
        name = os.path.basename(inputPath).split('.')[0]
        subFoldName = out + name
        if os.path.isdir(subFoldName) is False:
            os.mkdir(subFoldName)
        subFoldName += '/'
        #print(name)
        i = 0
        while True:
            ret, frame = source.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            if(i % freq == 0):
                framename = subFoldName + name + '_' + getSuffix(nDigits, i + entryIdx) + '.png'
            #print(framename)
                cv2.imwrite(framename, frame)
                print(".", end="", flush=True)
            i += 1
        print('Extract video {0} finished!', inputPath)
    
    print("Extract all videos finished!")