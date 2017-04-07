from core import audio2image, image2audio
import os
import json
import random

if __name__ == "__main__":
    IMAGE_PATH = "C:\\Users\\boddm\\Desktop\\work\\music-nerual-style\\dataset\\image"
    train_lst_file = open("dataset\\train.lst", "w")
    val_lst_file = open("dataset\\val.lst", "w")

    image_file_list = filter(lambda x:x.find("tiff")>0, os.listdir(IMAGE_PATH))

    count = 0
    type_set = set()
    type_list = []
    lines = []
    for i in image_file_list:

        image_type = i.split('.')[0]
        image_file = os.path.join(IMAGE_PATH, i)
        if not (image_type in type_set):
            type_set.add(image_type)
            type_list.append(image_type)

        line = "{}\t{}\t{}\n".format(count, type_list.index(image_type), image_file)
        lines.append(line)

        print("Working on '{}':'{}' ----\t{}/{}.".format(image_type, i, count, len(image_file_list)))
        count  = count + 1
    random.shuffle(lines)
    train_lst_file.writelines(lines[500:])
    val_lst_file.writelines(lines[:500])

    json.dump(type_list, open("type_list.json", "w"))

