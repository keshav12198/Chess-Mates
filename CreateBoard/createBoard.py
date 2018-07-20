import cv2
import numpy as np

w = cv2.imread('board.png',1)
b = cv2.imread('blackBox.png',1)
roi = b[0:85,0:85]

cv2.namedWindow('board',cv2.WINDOW_AUTOSIZE)
cv2.resizeWindow('board',680,680)

k = 85
l = 0
for i in range(1,9):
	for j in range(1,5):
		w[l:l+85, k:k+85] = roi
		k = k + 170
	if i%2 == 0:
		k = 85
	else:
		k = 0
	l = l + 85

cv2.imshow('board',w)
cv2.imwrite('finalBoard.jpg',w)
k = cv2.waitKey(0)

cv2.destroyAllWindows()
