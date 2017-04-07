import os

if __name__ == '__main__':
    BASE_PATH = 'C:/Users/boddm/Desktop/work/music-nerual-style/dataset/gulong'
    text_file_list = filter(lambda x:x.find('txt')>0, os.listdir(BASE_PATH))
    target_file = open('gulong.txt', 'w')
    count = 0
    for i in text_file_list:
        count = count + 1
        text_file = os.path.join(BASE_PATH, i)
        lines = open(text_file).readlines()
        lines = filter(lambda x:x[0]==' ', lines)
        lines = map(lambda x:x.lstrip(), lines)
        target_file.writelines(lines)
        if count > 4:
            break
    pass
