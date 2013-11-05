from PIL import Image
import numpy
import colorsys

def getHSVFromImage(fileName):
    src=Image.open(fileName)
    h=numpy.zeros((src.size[0],src.size[1]))
    s=numpy.zeros((src.size[0],src.size[1]))
    v=numpy.zeros((src.size[0],src.size[1]))

    r,g,b=src.convert("RGB").split()
    
    for x in xrange(src.size[0]):
        for y in xrange(src.size[1]):
            h[x][y]=colorsys.rgb_to_hsv(r.getpixel((x,y)),g.getpixel((x,y)),b.getpixel((x,y)))[0]*255
            s[x][y]=colorsys.rgb_to_hsv(r.getpixel((x,y)),g.getpixel((x,y)),b.getpixel((x,y)))[0]
            v[x][y]=colorsys.rgb_to_hsv(r.getpixel((x,y)),g.getpixel((x,y)),b.getpixel((x,y)))[0]
    return h,s,v

def getImageInfo(fileName):
    gap=10    
    h,s,v=getHSVFromImage(fileName)
    ImageAttr = numpy.zeros(h.shape[0]/gap * h.shape[1]/gap)
    index=0
    lightness=0
    for x in xrange(h.shape[0]/gap):
            for y in xrange(h.shape[1]/gap):
                    tempHSum = 0
                    for m in xrange(gap):
                            for n in xrange(gap):
                                    tempHSum += h[x * gap + m][y * gap + n]
                                    lightness += v[x * gap + m][y * gap + n]
                    tempHSum = int(tempHSum / gap / gap)
                    ImageAttr[index] = tempHSum
                    index += 1
    return lightness/h.size,ImageAttr

if __name__ == '__main__':
    a,b=getImageInfo('TheStarryNight.jpg')
