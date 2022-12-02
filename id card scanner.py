import cv2

card_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

img = cv2.imread('idcard.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cards = card_cascade.detectMultiScale(gray, 1.1, 6)

for(x,y,w,h) in cards:
    print(x, y, w, h)
    cv2.rectangle(img, (x,y), (x + w, y + h), (255, 0, 0), 2)

cv2.imshow('img', img)
cv2.waitKey()