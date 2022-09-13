import cv2
import numpy as np

frameWidth = 640
frameHeight = 480

cap = cv2.VideoCapture(2)
cap.set(3,frameWidth)
cap.set(4,frameHeight)
cap.set(10,150)

def preProcessing(img):
	imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)
	imgCanny = cv2.Canny(imgBlur,200,200)
	kernel = np.ones((5,5))
	imgDial = cv2.dilate(imgCanny, kernel, iterations = 2)
	imgThres = cv2.erode(imgDial, kernel,iterations = 1)
	return imgThres

def getContours(img):
	biggest = np.array([])
	maxArea = 0
	contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
	for cnt in contours:
		area = cv2.contourArea(cnt)
		# print(area)
		if area > 5000:
			# cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
			peri = cv2.arcLength(cnt, True)
			approx = cv2.approxPolyDP(cnt,0.02*peri,True)
			if area > maxArea and len(approx) == 4:
				biggest = approx
				maxArea = area
	cv2.drawContours(imgContour, biggest, -1, (255, 0, 0), 20)
	return biggest


def reorder(currentPoints):
	# print(currentPoints)
	try:
		currentPoints = currentPoints.reshape((4,2))
		currentPointsNew = np.zeros((4,1,2),np.int32)
		add = currentPoints.sum(1)
		currentPointsNew[0] = currentPoints[np.argmin(add)]
		currentPointsNew[3] = currentPoints[np.argmax(add)]
		diff = np.diff(currentPoints, axis = 1)
		currentPointsNew[1] = currentPoints[np.argmin(diff)]
		currentPointsNew[2] = currentPoints[np.argmax(diff)]
	except:
		return currentPoints
	return currentPointsNew



def getWarp(img, biggest):
	biggest = reorder(biggest)
	points1 = np.float32(biggest)
	points2 = np.float32([[0,0], [frameWidth,0],[0,frameHeight],[frameWidth,frameHeight]])
	try:
		matrix = cv2.getPerspectiveTransform(points1, points2)
		imgOutput = cv2.warpPerspective(img,matrix,(frameWidth,frameHeight))
	except:
		return img
	return imgOutput


while True:
	success, img = cap.read()
	cv2.resize(img,(frameWidth, frameHeight))
	imgContour = img.copy()
	imgThres = preProcessing(img)
	biggest = getContours(imgThres)

	imgWarped = getWarp(img, biggest)

	cv2.imshow("Skaner", imgWarped)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

