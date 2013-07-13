#!/usr/bin/python

import sys
import cv2.cv as cv
import numpy

def image_get_h(src):
	hsv = cv.CreateImage(cv.GetSize(src), 8, 3)
	cv.CvtColor(src, hsv, cv.CV_BGR2HSV)
	h_plane = cv.CreateMat(src.rows, src.cols, cv.CV_8UC1)
	cv.Split(hsv, h_plane, None, None, None)
	return h_plane

def image_get_v(src):
	hsv = cv.CreateImage(cv.GetSize(src), 8, 3)
	cv.CvtColor(src, hsv, cv.CV_BGR2HSV)
	v_plane = cv.CreateMat(src.rows, src.cols, cv.CV_8UC1)
	cv.Split(hsv, None, None, v_plane, None)
	return v_plane

def image_static_v(src):
	v_plane = image_get_v(src)
	temp = 0;
	for row in range(v_plane.rows):
		for col in range(v_plane.cols):
			temp += v_plane[row, col]
	return temp / (v_plane.rows * v_plane.cols * 255)

def image_resize(src, rows, cols):
	new_img0 = cv.CreateMat(rows, cols, cv.CV_8UC3)
	cv.Resize(src, new_img0)
	return new_img0

def image_handle(src):
	src_h = image_get_h(src)
	new_img_h = cv.CreateMat(src_h.rows, src_h.cols, cv.CV_8UC1)
	gap = 10
	row = src_h.rows / gap
	col = src_h.cols / gap
	temp = 0
	index = 0;
	new_array = numpy.zeros(src_h.rows * src_h.cols / (gap * gap))
	for i in range(row):
		for j in range(col):
			temp = 0
			for m in range(gap):
				for n in range(gap):
					temp += src_h[i * gap + m, j * gap + n]
			temp = int(temp / gap / gap)
			new_array[index] = temp
			index += 1
			for m in range(gap):
				for n in range(gap):
					new_img_h[i * gap + m, j * gap + n] = temp
	return new_array

def getImgLight(imgfile):
	src = cv.LoadImageM(imgfile)
	resized_img = image_resize(src, 500, 500)
	return image_static_v(resized_img)

def getImgAttr(imgfile):
	src = cv.LoadImageM(imgfile)
	resized_img = image_resize(src, 500, 500)
	return image_handle(resized_img)
