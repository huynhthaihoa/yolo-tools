import cv2
import argparse
import os 

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

def getTimeStamp(index, fps):
    '''
    get time stamp of the frame:
    @index [in]: frame index,
    @fps [in]: camera frame per second
    '''
    millisecond = int(index * (1000 / fps))
    second, millisecond = divmod(millisecond, 1000)
    minute, second = divmod(second, 60)
    hour, minute = divmod(minute, 60)
    return "{0:02d}h{1:02d}m{2:02d}s{3:03d}ms".format(hour, minute, second, millisecond)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", help="Path to the input video",
                    type=str, default="input.mp4")
    parser.add_argument("-o", "--output", help="Path to the output folder",
                    type=str, default="output")
    parser.add_argument("-e", "--entry", help="The first index of the image (default is 0)", 
                    type=int, default=0)
    parser.add_argument("-s", "--step", help="Distance between 2 adjacent saved frames (default is 1)", 
                    type=int, default=1)
    parser.add_argument("-p", "--prefix", help="Image prefix (prefix of extracted image name, default is video name)", 
                    type=str, default="")
    args = parser.parse_args()
    inputPath = args.input
    source = cv2.VideoCapture(inputPath)
    fps = source.get(cv2.CAP_PROP_FPS)
    nFrames = getFrameNum(inputPath)
    print("Frames:", nFrames)
    nDigits = countDigit(nFrames)
    print("# of digits:", nDigits)
    out = args.output
    if os.path.isdir(out) is False:
        os.mkdir(out)
    out += '/'
    entryIdx = args.entry
    freq = args.step
    prefix = args.prefix
    name = os.path.basename(inputPath).split('.')[0]
    if prefix != "":
        name = prefix
    i = 0
    while cv2.waitKey(1) < 0:
        ret, frame = source.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        framename = out + name + '_' + getTimeStamp(i, fps) + '.jpg' # getSuffix(nDigits, i + entryIdx) + '.png'
        cv2.imwrite(framename, frame)
        print(".", end="", flush=True)
        i += 1
    print('Extract video finished!')