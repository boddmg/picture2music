import scipy.io.wavfile
import os
import numpy as np

def main():
    MUSIC_PATH = "C:\\Users\\boddm\\Desktop\\work\\music-nerual-style\\dataset\\music"
    MUSIC_ORIGIN_PATH = "C:\\Users\\boddm\\Desktop\\work\\music-nerual-style\\dataset\\music-origin"

    music_file_list = filter(lambda x:x.find("wav")>0, os.listdir(MUSIC_ORIGIN_PATH))

    count = 0
    for i in music_file_list:
        count = count + 1
        music_file = os.path.join(MUSIC_ORIGIN_PATH, i)
        rate, data =  scipy.io.wavfile.read(music_file)
        length = data.shape[0]
        step = length/5
        datas = np.split(data, range(0, length, step))
        base_name = os.path.splitext(i)[0]
        ext = os.path.splitext(i)[1]
        name_count = 0
        for j in datas:
            if j.shape[0] > 10000:
                name_count = name_count + 1
                scipy.io.wavfile.write(os.path.join(MUSIC_PATH, "{}-{}{}".format(base_name, name_count, ext)), rate, j)
        print("Working on '{}' ----\t{}/{}.".format(i, count, len(music_file_list)))



if __name__ == "__main__":
    main()
    pass