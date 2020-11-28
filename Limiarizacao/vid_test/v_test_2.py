import cv2 as cv
import numpy as np

def get_vid_info(cap):
  vid_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
  vid_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
  vid_fps = cap.get(cv.CAP_PROP_FPS)
  return vid_width, vid_height, vid_fps

def calc_hist(img, img_size):
    hist = [0]*256
    for i in range(img_size):
        hist[img[i]] += 1
    return hist

def calc_limiar(hist, l, err, is_diff_abs):
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

def create_binary(img, img_size, l):
    new_img = np.array([0]*img_size, dtype='uint8')
    for i in range(img_size):
        if (img[i] > l):
            new_img[i] = 255
    return new_img

cap = cv.VideoCapture('teste.mp4')

vid_width, vid_height, vid_fps = get_vid_info(cap)

# Para arquivos .avi
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('b.avi', fourcc, vid_fps, (vid_width, vid_height), isColor=False)

# Para arquivos .mp4
#fourcc = cv.VideoWriter_fourcc(*'mp4v')
#out = cv.VideoWriter('b.mp4', fourcc, vid_fps, (vid_width, vid_height), isColor=False)

while(True):
    ret, frame = cap.read()
    if (ret):
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        n_linhas, n_colunas = gray.shape
        print("Shape: ", gray.shape)
        v_gray = gray.reshape(n_linhas*n_colunas)
        print("V_gray: ", v_gray.size)
        hist = calc_hist(v_gray, v_gray.size)
        l = calc_limiar(hist, 127, 5, True)
        new_img_v = create_binary(v_gray, v_gray.size, l)
        print('dtype ', new_img_v.dtype)
        new_img = new_img_v.reshape((n_linhas, n_colunas))
        out.write(new_img)
    else: 
        break

cap.release()
out.release()
print("done.")
