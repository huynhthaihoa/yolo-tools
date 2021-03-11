import numpy as np
import cv2
import tensorflow as tf
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

def from_yolo(x, y, w, h):
    '''
    Convert bounding box info from Yolo format to tf format:
    @x [in]:
    @y [in]:
    @w [in]:
    @h [in]:
    @xmin [out]:
    @xmax [out]:
    @ymin [out]:
    @ymax [out]:
    '''
    x = float(x)
    y = float(y)
    w = float(w)
    h = float(h)
    xmax = x + w / 2.0
    xmin = x - w / 2.0
    ymax = y + h / 2.0
    ymin = y - h / 2.0
    return [ymin, xmin, ymax, xmax]

def to_yolo(ymin, xmin, ymax, xmax):
    '''
    Convert bounding box info from tf format to Yolo format:
    @ymin [in]:
    @xmin [in]:
    @ymax [in]:
    @xmax [in]:
    @x [out]:
    @y [out]:
    @w [out]:
    @h [out]:
    '''
    x = (xmax + xmin) / 2.0
    w = (xmax - xmin)
    y = (ymax + ymin) / 2.0 
    h = (ymax - ymin)
    return [x, y, w, h]


def convert_from_yolo(line): # [id, x_min, y_min, w, h] -> [y_min, x_min, y_max, x_max]
    raws = line.split(' ')
    elems = from_yolo(raws[1], raws[2], raws[3], raws[4])
    #elems = [float(raws[2]), float(raws[1]), float(raws[2]) + float(raws[3]), float(raws[2]) + float(raws[1])]
    _id = int(raws[0])
    return elems, _id

def convert_to_yolo(line, _id): # [y_min, x_min, y_max, x_max] -> [id, x_min, y_min, w, h]
    #elems = [_id, line[1], line[0], line[3] - line[1], line[2] - line[0]]
    elems = to_yolo(line[0], line[1], line[2], line[3])
    elems.insert(0, _id)
    return elems

def bbox_conversion(lines):
    # bboxes = list()
    # ids = list()
    bboxes = dict()
    for line in lines:
        _bbox, _id = convert_from_yolo(line)
        bboxes[_id].append(_bbox)
        # bboxes.append(_bbox)
        # ids.append(_id)
    return bboxes#, ids

#tf.config.run_functions_eagerly(False)

img = cv2.imread('demo\APHU7299440_9-0.jpg')
print(np.shape(img))
ann = open("demo\APHU7299440_9-0.txt", "rt")
lines = list()
for line in ann:
    lines.append(line)
boxes, ids = bbox_conversion(lines)
bboxes = tf.constant([boxes])

begin, size, bbox_for_draw = tf.image.sample_distorted_bounding_box(tf.shape(img), bounding_boxes=bboxes, min_object_covered=0.1)
# colors = np.array([[1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
# image_with_box = tf.image.draw_bounding_boxes(tf.expand_dims(img, 0), bbox_for_draw, colors)
# tf.compat.v1.summary.image('images_with_box', image_with_box)
distorted_image = tf.slice(img, begin, size)
distorted_image = distorted_image.numpy()
print(bbox_for_draw)
# print(distorted_image.numpy())
#cv2.imwrite("new.jpg",np.ndarray(distorted_image))
distorted_bboxes = bbox_for_draw.numpy()
distorted_bboxes = np.squeeze(distorted_bboxes, axis=0)
print(np.squeeze(distorted_bboxes, axis=0))
print(np.shape(distorted_image))
cv2.imwrite("new.jpg", distorted_image)

h, w, _ = distorted_image.shape
for i, box in enumerate(distorted_bboxes): #[y_min, x_min, y_max, x_max] -> (x, y), (x+w, y+h)
    x = int(box[1] * w) 
    y = int(box[0] * h)
    xm = int(box[3] * h) 
    ym = int(box[2] * h)
    cropImg = distorted_image[y : ym, x : xm]
    cv2.imwrite("new-{0}.jpg".format(i), cropImg)
    #x = box[1] * 
    # x = int(distorted_image.shape[0] * box[1])
    # y = int(distorted_image.shape[1] * box[0])
    # xm = int(distorted_image.shape[0] * box[3])
    # ym = int(distorted_image.shape[1] * box[2])
    # print("x,y,xm,ym:",x,y,xm,ym)
    # cv2.rectangle(distorted_image, (x, y), (xm, ym), (0, 0, 255), 2)
    # cv2.rectangle(distorted_image, (y, x), (ym, xm), (0, 255, 0), 2)

# cv2.imwrite("new-2.jpg", distorted_image)#.numpy())

# h, w, _ = img.shape
# for box in boxes: #[y_min, x_min, y_max, x_max] -> (x, y), (x+w, y+h)
    
#     #x = box[1] * 
#     x = int(img.shape[0] * box[1])
#     y = int(img.shape[1] * box[0])
#     xm = int(img.shape[0] * box[3])
#     ym = int(img.shape[1] * box[2])
#     print("x,y,xm,ym:",x,y,xm,ym)
#     # cv2.rectangle(img, (h - xm, h - ym), (h - x, h - y), (255, 0, 0), 2)
#     # cv2.rectangle(img, (x, y), (xm, ym), (0, 0, 255), 2)
#     cv2.rectangle(img, (h - ym, w - xm), (h - y, w - x), (0, 255, 0), 2)
#     cv2.rectangle(img, (w - ym, h - xm), (w - y, h - x), (0, 255, 0), 2)

# cv2.imwrite("origin.jpg", img)
# cv2.imshow("bounding_box", distorted_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()