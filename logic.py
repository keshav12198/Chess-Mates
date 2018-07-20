import cv2

def set(roi,k,c):
	gray = cv2.cvtColor(k,cv2.COLOR_BGR2GRAY)
	if c == 0:
		ret, th1 = cv2.threshold(gray,3,255,cv2.THRESH_BINARY)
	elif c == 1:
		ret, th1 = cv2.threshold(gray,220,255,cv2.THRESH_BINARY)
	fg = cv2.bitwise_and(k,k,mask = th1)
	th2 = cv2.bitwise_not(th1)
	bg = cv2.bitwise_and(roi,roi,mask = th2)
	ans = cv2.add(fg,bg)
	return ans

def isNotCheck(refPt,mat,turn,afterCheck):
	if turn == 0:
		ch1 = 'B'
		ch2 = 'W'
	if turn == 1:
		ch1 = 'W'
		ch2 = 'B'
	w,h = 8,8
	mat2 = [["nil" for x in range(w)] for y in range(h)]
	for fir in range(0,8):
		for sec in range(0,8):
			mat2[fir][sec] = mat[fir][sec]
	if afterCheck == 0:
		ptx, pty = refPt[0]
		i, j = pty/85, ptx/85
		ptx1, pty1 = refPt[1]
		m, n = pty1/85, ptx1/85
		name = mat2[i][j]
		mat2[i][j] = 'nil'
		mat2[m][n] = name
	for i in range(0,8):
		for j in range(0,8):
			if mat2[i][j] == ('kg'+ch1):
				e = i
				f = j
	refPts = [(0,0)]
	refPts.append((f*85,e*85))	
	for x in range(0,8):
		for y in range(0,8):
			names = mat2[x][y]
			if names[2] == ch2:
				refPts[0] = ((y*85,x*85))
				val = isValid(names,'kg'+ch1,mat2,refPts)
				if val == True:
					return False
	return True

def isValid(name1,name2,mat,refPt):
	ptx, pty = refPt[0]
	i, j = pty/85,ptx/85
	ptx1, pty1 = refPt[1]
	m, n = pty1/85,ptx1/85

	if i == m and j == n:
		return False

	if name1[0] == 'q' and name1[1] == 'n':
		ptr1 = isValid("bp",name2,mat,refPt)
		ptr2 = isValid("rk",name2,mat,refPt)
		if ptr1 == True or ptr2 == True:
			first = True
		else:
			first = False
		return first

	if name1[0] == 'k' and name1[1] == 't':
		if n == j+2 or n == j-2:
			if m == i-1 or m == i+1:
				return True
		if m == i-2 or m == i+2:
			if n == j+1 or n == j-1:
				return True
		return False

	elif (name1[0] == 'b' and name1[1] == 'p'):
		if (m-n) == (i-j):
			if m > i:
				i = i + 1
				j = j + 1
				while(i!=m):
					if mat[i][j] != 'nil':
						return False
					i = i + 1
					j = j + 1
			else:
				i = i - 1
				j = j - 1
				while(i!=m):
					if mat[i][j] != 'nil':
						return False
					i = i - 1
					j = j - 1
			return True
		elif (m+n) == (i+j):
			if m > i:
				i = i + 1
				j = j - 1
				while(i!=m):
					if mat[i][j] != 'nil':
						return False
					i = i + 1
					j = j - 1
			else:
				i = i - 1
				j = j + 1
				while(i!=m):
					if mat[i][j] != 'nil':
						return False
					i = i - 1
					j = j + 1
			return True
		return False

	elif (name1[0] == 'r' and name1[1] == 'k'):
		if i == m:
			if n > j:
				j = j + 1
				while(j!=n):
					if mat[i][j] != 'nil':
						return False
					j = j + 1
			else:
				j = j - 1
				while(j!=n):
					if mat[i][j] != 'nil':
						return False
					j = j - 1
			return True
		elif j == n:
			if m > i:
				i = i + 1
				while(i!=m):
					if mat[i][j] != 'nil':
						return False
					i = i + 1
			else:
				i = i - 1
				while(i!=m):
					if mat[i][j] != 'nil':
						return False
					i = i - 1
			return True
		return False

	elif name1[0] == 'p' and name1[1] == 'n' and name1[2] == 'W':
		if i == 6 and m == 4 and mat[m][n] == 'nil' and mat[m+1][n] == 'nil':
			return True
		if m == i-1 and n == j and mat[m][n] == 'nil':
			return True
		if (m == i-1) and (n == j+1 or n == j-1):
			if name1[2] == 'B' and name2[2] == 'W':
				return True
			if name1[2] == 'W' and name2[2] == 'B':
				return True
		return False

	elif name1[0] == 'p' and name1[1] == 'n' and name1[2] == 'B':
		if i == 1 and m == 3 and mat[m][n] == 'nil' and mat[m-1][n] == 'nil':
			return True
		if m == i+1 and n == j and mat[m][n] == 'nil':
			return True
		if (m == i+1) and (n == j+1 or n == j-1):
			if name1[2] == 'B' and name2[2] == 'W':
				return True
			if name1[2] == 'W' and name2[2] == 'B':
				return True
		return False

	elif name1[0] == 'k' and name1[1] == 'g':
		if (m == i) or (m == i+1) or (m == i-1):
			if (n == j) or (n == j+1) or (n == j-1):
				return True
		return False

	else:
		return False

def forPawn(turn,r1,r2,c1,c2,cur,light,dark):
	while(True):
		print "Which piece should be born again?"
		print "Type qn for Queen"
		print "Type kt for Knight"
		print "Type bp for Bishop"
		print "Type rk for Rook"
		ans1 = raw_input()
		if ans1 == "qn" or ans1 == "kt" or ans1 == "bp" or ans1 == "rk":
			break
	if abs(r1-c1)&1 == 0:
		cur[r1:r2,c1:c2] = light
	else:
		cur[r1:r2,c1:c2] = dark
	if turn == 0:
		ans1 = ans1 + 'B'
	else:
		ans1 = ans1 + 'W'
	print ans1
	roi = cur[r1:r2,c1:c2]
	imgNew = cv2.imread(ans1+'.png',1)
	return set(roi,imgNew,turn),ans1

