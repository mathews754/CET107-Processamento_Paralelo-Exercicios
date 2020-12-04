import numpy as np
cimport numpy as np
import pymp

DTYPE = np.uint8
# ctypedef np.uint8_t DTYPE_t

def calc_hist(np.ndarray img, long int img_size):
    cdef long int hist[256]
    cdef int i = 0

    for i in range(256):
        hist[i] = 0
    for i in range(img_size):
        hist[img[i]] += 1
    return hist

def calc_hist_par(np.ndarray img, long int img_size, short int n_threads):
    cdef long int i
    cdef short int j
    hist = pymp.shared.array((256,), dtype='uint32')
    with pymp.Parallel(n_threads) as p:
        p_hist = [0]*256
        for i in p.range(img_size):
            p_hist[img[i]] += 1
        for j in range(256):
            with p.lock:
                hist[j] += p_hist[j]
    return hist

def calc_limiar(hist, float l, float err, int is_diff_abs):
    cdef float diff, l1
    cdef long int somaMenor, somaMaior, contaMenor, contaMaior 
    cdef short int i
    diff = err
    while (diff >= err):
        somaMenor = somaMaior = contaMenor = contaMaior = 0
        for i in range(int(l)):
            somaMenor += hist[i]*i
            contaMenor += hist[i]
        for i in range(int(l), 256):
            somaMaior += hist[i]*i
            contaMaior += hist[i]
        l1 = (somaMaior/contaMaior+somaMenor/contaMenor)/2
        if (is_diff_abs):
            diff = abs(l1 - l)
        else:
            diff = abs(l1 - l)/l
        l = l1
    return l

def create_binary(np.ndarray img, int img_size, float l):
    cdef long int i = 0
    cdef np.ndarray new_img = np.zeros((img_size,), dtype=DTYPE) 
    # cdef np.ndarray new_img = np.array([0]*img_size, dtype=DTYPE)
    for i in range(img_size):
        if (img[i] > l):
            new_img[i] = 255
        # else:
        #     new_img[i] = 0
    return new_img

def create_binary_par(img, long int img_size, float l, short int n_threads):
    cdef long int i = 0
    cdef np.ndarray new_img
    new_img = pymp.shared.array((img_size,), dtype='uint8')
    with pymp.Parallel(n_threads) as p:
        for i in p.range(img_size):
            if (img[i] > l): 
                new_img[i] = 255
            else: 
                new_img[i] = 0
    return new_img
