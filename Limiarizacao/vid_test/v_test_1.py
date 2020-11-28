import cv2 as cv
import numpy as np

def get_vid_info(cap):
  vid_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
  vid_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
  vid_fps = cap.get(cv.CAP_PROP_FPS)
  return vid_width, vid_height, vid_fps


cap = cv.VideoCapture('vid.mp4')
print(cap.get(cv.CAP_PROP_FOURCC))
print(cap.get(cv.CAP_PROP_FPS))
print(cap.get(cv.CAP_PROP_FRAME_COUNT))
print(cap.get(cv.CAP_PROP_FRAME_WIDTH))
print(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

vid_width, vid_height, vid_fps = get_vid_info(cap)

# Para arquivos .avi
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('output.avi', fourcc, vid_fps, (vid_width, vid_height), isColor=False)

# Para arquivos .mp4
# fourcc = cv.VideoWriter_fourcc(*'mp4v')
# out = cv.VideoWriter('output.mp4', fourcc, vid_fps, (vid_width, vid_height), isColor=False)

while(True):
    ret, frame = cap.read()
    if (not ret): break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    out.write(gray)

cap.release()
out.release()
print("done.")
