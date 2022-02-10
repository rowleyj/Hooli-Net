import cv2
import imutils
import numpy as np
import pytesseract
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\tnaguib\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

img = cv2.imread('src\modules\models\plates\platevidcrop.png',cv2.IMREAD_COLOR)

img = cv2.resize(img, (700,700) )

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert to grey scale
gray = cv2.bilateralFilter(gray, 100, 77, 77) #Blur to reduce noise
cv2.imshow('gray',gray)
edged = cv2.Canny(gray, 30, 250) #Perform Edge detection
cv2.imshow('edged',edged)
# find contours in the edged image, keep only the largest
# ones, and initialize our screen contour
cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
screenCnt = None


for c in cnts:
  for eps in np.linspace(0.001, 0.05, 20):
    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, eps * peri, True)
    # draw the approximated contour on the image
    output = img.copy()
    cv2.drawContours(output, [approx], -1, (0, 255, 0), 3)
    #cv2.imshow("Approximated Contour", output)
    if len(approx) == 5:
      screenCnt = approx
      # Masking the part other than the number plate
      mask = np.zeros(gray.shape,np.uint8)
      new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
      new_image = cv2.bitwise_and(output,img,mask=mask)

      # Now crop
      (x, y) = np.where(mask == 255)
      (topx, topy) = (np.min(x), np.min(y))
      (bottomx, bottomy) = (np.max(x), np.max(y))
      Cropped = gray[topx:bottomx+1, topy:bottomy+1]

      #Read the number plate
      text = pytesseract.image_to_string(Cropped, config='--psm 11')
      if len(text)>3:
        print("Detected Number is:",text)      
        cv2.imshow('image',output)
        cv2.imshow('Cropped',Cropped)

        cv2.waitKey(0)
"""
# loop over our contours
for c in cnts:
 # approximate the contour
 peri = cv2.arcLength(c, True)
 approx = cv2.approxPolyDP(c, 0.018* peri, True)
 
 # if our approximated contour has four points, then
 # we can assume that we have found our screen
 if len(approx) == 4:
  break

if screenCnt is None:
 detected = 0
 print("No contour detected")
else:
 detected = 1

if detected == 1:
  cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)
"""
