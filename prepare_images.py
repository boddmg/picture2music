from core import audio2image, image2audio
import os

if __name__ == "__main__":
    MUSIC_PATH = "C:\\Users\\boddm\\Desktop\\work\\music-nerual-style\\dataset\\music"
    OUT_MUSIC_PATH = "C:\\Users\\boddm\\Desktop\\work\\music-nerual-style\\result"
    IMAGE_PATH = "C:\\Users\\boddm\\Desktop\\work\\music-nerual-style\\dataset\\image"

    music_file_list = filter(lambda x:x.find("wav")>0, os.listdir(MUSIC_PATH))

    count = 0
    for i in music_file_list:
        count  = count+1
        image_file = i.replace('wav', 'tiff')
        music_file = os.path.join(MUSIC_PATH, i)
        out_music_file = os.path.join(OUT_MUSIC_PATH, i)
        image_file = os.path.join(IMAGE_PATH, image_file)
        print("Working on '{}' ----\t{}/{}.".format(i, count, len(music_file_list)))
        # if count < 200:
        #     continue
        audio2image(music_file, image_file)
        image2audio(image_file, out_music_file)
        # if count>2:
        #     break

