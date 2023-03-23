# 来源：https://www.bilibili.com/video/BV1Bv411H7ER?p=5

import xml.etree.ElementTree as ET
from os import getcwd
import glob

classes = ['crazing', 'inclusion', 'patches', 'pitted_surface', 'rolled-in_scale', 'scratches']


def convert(size, box):
    delta_w = 1. / size[0]
    delta_h = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * delta_w
    w = w * delta_w
    y = y * delta_h
    h = h * delta_h
    return x, y, w, h


def convert_annotation(image_name):
    in_file = open('./ANNOTATIONS/' + image_name[:-3] + 'xml')
    out_file = open('./labels/' + image_name[:-3] + 'txt', 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls not in classes:
            print(cls)
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


wd = getcwd()

if __name__ == '__main__':
    for image_path in glob.glob('./ANNOTATIONS/*.xml'):
#       获取文件名
        image_name = image_path.split('\\')[-1]
# 		转换
        convert_annotation(image_name)

