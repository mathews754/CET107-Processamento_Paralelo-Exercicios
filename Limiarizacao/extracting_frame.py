import cv2

vidcap = cv2.VideoCapture('archive_name.mp4') #reading video
success, image = vidcap.read()
count=0
while success:
	success, image = vidcap.read()
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	cv2.imwrite("frame%d.jpg" % count, image) #creating enumerated frames
	if cv2.waitKey(10)==27:
		break
	count+=1
