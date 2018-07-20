#Castling remaining

import cv2
from logic import *

cv2.namedWindow("board")
light = cv2.imread('lightBox.png',1)
dark = cv2.imread('darkBox.png',1)

turn = 1
check = -1

def getImage(name):
	# print name
	if name[2] == 'B':
		c = 0
	elif name[2] == 'W':
		c = 1
	else:
		c = -1
	img = cv2.imread(name+'.png',1)
	return img, c

f1 = False
done = False

def click_and_crop(event, x, y, flags, param):

	global f1, done, refPt, name, img, c, turn

	if event == cv2.EVENT_LBUTTONDOWN:
		refPt = [(x, y)]
		name = mat[y/85][x/85]
		if turn == 0 and name[2] == 'W':
			pass
		elif turn == 1 and name[2] == 'B':
			pass
		elif name == 'nil':
			pass
		else:
			c1 = (x/85)*85
			r1 = (y/85)*85
			r2 = r1 + 85
			c2 = c1 + 85
			if abs(r1-c1)&1 == 0:
				b[r1:r2,c1:c2] = light
			else:
				b[r1:r2,c1:c2] = dark
			cv2.imwrite('current.jpg',b)
			img, c = getImage(name)
			f1 = True

	elif event == cv2.EVENT_MOUSEMOVE:
		if f1 == True:
			cur = cv2.imread('current.jpg',1)
			r1 = y - 42
			c1 = x - 42
			r2 = y + 43
			c2 = x + 43
			roi =  cur[r1:r2,c1:c2]
			if c!=-1:
				ans = set(roi,img,c)
				b[r1:r2,c1:c2] = ans
		elif f1 == False:
			pass

	elif event == cv2.EVENT_LBUTTONUP:
		if f1 == True:
			refPt.append((x,y))
			name2 = mat[y/85][x/85]
			r1 = (y/85)*85
			r2 = r1 + 85
			c1 = (x/85)*85
			c2 = c1 + 85
			first = isValid(name,name2,mat,refPt)
			if name2[2] == 'B' and turn == 0:
				second = False
			elif name2[2] == 'W' and turn == 1:
				second = False
			else:
				second = True
			if first == True and second == True:
				third = isNotCheck(refPt,mat,turn,0)
			else:
				third = False
			p,q = refPt[0]
			if first == True and second == True and third == True:
				mat[y/85][x/85] = name
				mat[q/85][p/85] = "nil"
			else:
				r1 = (q/85)*85
				r2 = r1 + 85
				c1 = (p/85)*85
				c2 = c1 + 85
			cur = cv2.imread('current.jpg',1)
			if c!=-1:	
				if abs(r1-c1)&1 == 0:
					cur[r1:r2,c1:c2] = light
				else:
					cur[r1:r2,c1:c2] = dark
				roi = cur[r1:r2,c1:c2]
				ans = set(roi,img,c)
				cur[r1:r2,c1:c2] = ans
				b[0:680,0:680] = cur[0:680,0:680]
			f1 = False
			done = True
			ck = -1
			if first == True and second == True and third == True:
				if (name == "pnB" and (y/85) == 7) or (name == "pnW" and (y/85) == 0):
					imgNew, ans1 = forPawn(turn,r1,r2,c1,c2,cur,light,dark)
					cur[r1:r2,c1:c2] = imgNew
					print "Done"
					b[r1:r2,c1:c2] = imgNew
					mat[y/85][x/85] = ans1

				if turn == 0:
					fourth = isNotCheck(refPt,mat,1,1)
					if fourth == False:
						ck = 1
					turn = 1
				else:
					fourth = isNotCheck(refPt,mat,0,1)
					if fourth == False:
						ck = 0
					turn = 0
			for fir in range(0,8):
				s = ""
				for sec in range(0,8):
					s = s + mat[fir][sec] + ' '
				print s
			if ck == 0:
				print "Check for Black"
			elif ck == 1:
				print "Check for White"
			else:
				pass

cv2.setMouseCallback("board", click_and_crop)

b = cv2.imread('basic.jpg',1)
w,h = 8,8
mat = [["nil" for x in range(w)] for y in range(h)]
mat[0][0] = mat[0][7] = "rkB"
mat[0][1] = mat[0][6] = "ktB"
mat[0][2] = mat[0][5] = "bpB"
mat[0][3] = "qnB"
mat[0][4] = "kgB"
for i in range(0,8):
	mat[1][i] = "pnB"

mat[7][0] = mat[7][7] = "rkW"
mat[7][1] = mat[7][6] = "ktW"
mat[7][2] = mat[7][5] = "bpW"
mat[7][3] = "qnW"
mat[7][4] = "kgW"
for i in range(0,8):
	mat[6][i] = "pnW"

cv2.imwrite('current.jpg',b)
while True:
	cv2.imshow('board',b)
	k = cv2.waitKey(1) & 0xFF
	if done == True:
		cv2.imwrite('current.jpg',b)
		done = False
	if k == ord('q'):
		break

cv2.destroyAllWindows()