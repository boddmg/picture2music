import cv2
import numpy as np
import scipy.io.wavfile
import scipy.misc
import tifffile
import math
import logging

import stft
from utility import pcm2float, float2pcm

image_width = 200.5
fs = 11025
frame_length = image_width / fs
T = image_width * frame_length
# T = 32.67 # sample time
# frame_length = math.sqrt(T/float(fs))

hop_length = frame_length # forget it

MAX = 2**8

# def normal(x):
#     print(np.min(x))
#     print(np.max(x))
#     x = x - np.min(x)
#     x = x / np.max(x)
#     return x
#
# def inv_normal(x):
#     print(np.min(x))
#     print(np.max(x))
#     x = x * MAX - 127
#     return x

normal = lambda x:(x+100)/200
inv_normal = lambda x:x*200 - 100

def debug_print(*args, **kwargs):
    # print(args, kwargs)
    pass

def save_image(data, file_name):
    debug_print(data.dtype, data.shape)
    tifffile.imsave(file_name, data)
    pass

def read_image(file_name):
    return tifffile.imread(file_name)

def P2R(radius, angles):
    return radius * np.exp(1j*angles)

def R2P(x):
    return np.absolute(x), np.angle(x)


def audio2image(audio_filename, image_filename):
    rate, data =  scipy.io.wavfile.read(audio_filename)
    debug_print(data.dtype)

    if len(data.shape) > 1:
        data = data[:,0]
    assert isinstance(data, np.ndarray)
    data = pcm2float(data)
    x = data
    x = x[:int(T*rate)]
    X = stft.stft(x, fs, frame_length, hop_length)

    debug_print(np.max(X.real),np.min(X.real))
    debug_print(np.max(X.imag),np.min(X.imag))
    r = normal(np.absolute(X)) * MAX
    g = normal(np.angle(X)) * MAX
    debug_print(r, g)
    X_image = cv2.merge([r, g, np.zeros(X.shape[:2])])
    # X_image = cv2.merge([normal(X.real) * 65535, normal(X.imag) * 65535, np.zeros(X.shape[:2])])
    X_image = X_image.astype('uint8')
    debug_print("finished stft.")
    # Plot the magnitude spectrogram.
    save_image(X_image,image_filename)

def image2audio(image_filename, audio_filename):
    X_image = read_image(image_filename)
    debug_print("show result of stft.")

    debug_print(X_image.dtype, X_image.shape)
    r = inv_normal(X_image[:,:,0].astype('float64') / MAX)
    g = inv_normal(X_image[:,:,1].astype('float64') / MAX)
    X = P2R(r, g)
    # X = np.zeros(X_image.shape[:2], 'complex128')
    # X.real = r
    # X.imag = g
    debug_print(np.max(X.real),np.min(X.real))
    debug_print(np.max(X.imag),np.min(X.imag))
    # Compute the ISTFT.
    xhat = stft.istft(X, fs, T, hop_length)
    xhat = float2pcm(xhat)
    scipy.io.wavfile.write(audio_filename, fs, xhat)

if __name__ == '__main__':
    sample_file = 'Duke Ellington - Rext.wav'
    audio2image(sample_file, 'test1.tiff')
    image2audio('test1.tiff', 'after-' + sample_file)
