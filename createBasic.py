import cv2

def set(roi,k,c):
	gray = cv2.cvtColor(k,cv2.COLOR_BGR2GRAY)
	if c == 0:
		val = 3
	else:
		val = 220
	ret, th1 = cv2.threshold(gray,val,255,cv2.THRESH_BINARY)
	fg = cv2.bitwise_and(k,k,mask = th1)
	th2 = cv2.bitwise_not(th1)
	bg = cv2.bitwise_and(roi,roi,mask = th2)
	ans = cv2.add(fg,bg)
	return ans

w, h = 8, 8;
Matrix = [['a' for x in range(w)] for y in range(h)]

b = cv2.imread('finalBoard.jpg',1)

for i in range(0,8):
	r1 = i*85
	r2 = r1 + 85
	if i == 0 or i == 7:
		c = 0
		if i == 7:
			c = 1
		#Put in 1st and last row
		for j in range(0,8):
			c1 = j*85
			c2 = c1 + 85
			if j == 0 or j == 7:
				if c == 0:
					r = cv2.imread('rookBlack.png',1)
				else:
					r = cv2.imread('rookWhite.png',1)
				ans = set(b[r1:r2,c1:c2],r,c)
				b[r1:r2,c1:c2] = ans
			elif j == 1 or j == 6:
				if c == 0:
					bsp = cv2.imread('knightBlack.png',1)
				else:
					bsp = cv2.imread('knightWhite.png',1)
				ans = set(b[r1:r2,c1:c2],bsp,c)
				b[r1:r2,c1:c2] = ans
			elif j == 2 or j == 5:
				if c == 0:
					bsp = cv2.imread('bishopBlack.png',1)
				else:
					bsp = cv2.imread('bishopWhite.png',1)
				ans = set(b[r1:r2,c1:c2],bsp,c)
				b[r1:r2,c1:c2] = ans
			elif j == 3:
				if c == 0:
					qn = cv2.imread('queenBlack.png',1)
				else:
					qn = cv2.imread('queenWhite.png',1)
				ans = set(b[r1:r2,c1:c2],qn,c)
				b[r1:r2,c1:c2] = ans
			elif j == 4:
				if c == 0:
					kg = cv2.imread('kingBlack.png',1)
				else:
					kg = cv2.imread('kingWhite.png',1)
				ans = set(b[r1:r2,c1:c2],kg,c)
				b[r1:r2,c1:c2] = ans

	elif i == 1 or i == 6:
		c = 0
		if i == 6:
			c = 1
		for j in range(0,8):
			c1 = j*85
			c2 = c1 + 85
			if c == 0:
				pn = cv2.imread('pawnBlack.png',1)
			else:
				pn = cv2.imread('pawnWhite.png',1)
			ans = set(b[r1:r2,c1:c2],pn,c)
			b[r1:r2,c1:c2] = ans


cv2.imshow('board',b)
cv2.imwrite('basic.jpg',b)
cv2.waitKey(0)
cv2.destroyAllWindows()