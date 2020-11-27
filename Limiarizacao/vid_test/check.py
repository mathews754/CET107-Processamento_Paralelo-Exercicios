import cv2 as cv
import numbers as np

cap = cv.VideoCapture('output.avi')
print(cap.get(cv.CAP_PROP_FOURCC))
print(cap.get(cv.CAP_PROP_FPS))
print(cap.get(cv.CAP_PROP_FRAME_COUNT))
print(cap.get(cv.CAP_PROP_FRAME_WIDTH))
print(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

while (True):
  ret, frame = cap.read()
  if (not ret): break
  print(frame)
#Fim

cap.release()
# cv.destroyAllWindows()
print("done.")