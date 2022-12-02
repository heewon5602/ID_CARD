import cv2
import os
import numpy as np

path = os.path.dirname(os.path.realpath(__file__)) + "/f.jpg"

img = cv2.imread('idcard.dooly.jpg')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5,5), 0)  #글자 영역 검출 개수를 줄여줌

mser = cv2.MSER_create() #mser: 글자 영역 검출 알고리즘
regions,_=mser.detectRegions(gray)

clone = img.copy()

hulls = [cv2.convexHull(p.reshape(-1, 1, 2)) for p in regions]

remove1 = []
for i, c1 in enumerate(hulls):  #검출된 convexhull에 존재하는 사각형들을 비교하는 알고리즘

    x, y, w, h = cv2.boundingRect(c1)
    r1_start = (x, y)
    r1_end = (x+w, y+h)
    
    for j,c2 in enumerate(hulls):

        if i == j:
            continue

        x, y, w, h = cv2.boundingRect(c2)
        r2_start = (x,y)
        r2_end = (x+w, y+h)
        
        if r1_start[0]>r2_start[0] and r1_start[1] > r2_start[1] and r1_end[0]<r2_end[0] and r1_end[1] < r2_end[1]:  #큰 사각형 안에 작은 사각형 존재 여부 검사
            remove1.append(i) #위의 조건이 충족된 경우 제거 대상에 해당 영역 추가

for j,cnt in enumerate(hulls):
    if j in remove1: continue
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(clone,(x, y), (x+w, y+h), (0,255,0), 1)

title='mosaic'
while True:
    x,y,w,h = cv2.selectROI(title, clone, False) 
    if w and h:
        roi = clone[y:y+h, x:x+w]   
        roi = cv2.resize(roi, (w//15, h//15)) 
        roi = cv2.resize(roi, (w,h), interpolation=cv2.INTER_AREA)  
        clone[y:y+h, x:x+w] = roi   
        cv2.imshow(title, clone) 
    else:
        break
    
cv2.imshow('mser', clone)
cv2.waitKey(0)
cv2.destroyAllWindows()