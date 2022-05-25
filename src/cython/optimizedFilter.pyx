# cython: language_level=3 
import cv2 
import math


cpdef unsigned char[:, :] quantize_gray(unsigned char [:, :] frame_gray, int n_levels):
    cdef int x, y, w, h
    h = frame_gray.shape[0]
    w = frame_gray.shape[1]
    for y in range(0, h):
        for x in range(0, w):
            frame_gray[y, x] = round(frame_gray[y, x] * n_levels / 255) * 255 / n_levels
    return frame_gray

