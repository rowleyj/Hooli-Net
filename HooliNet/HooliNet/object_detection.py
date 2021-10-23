import cv2

img_file = "HooliNet\HooliNet\car3.jpg"
img = cv2.imread(img_file)

car_classifier = 'HooliNet\HooliNet\cars.xml'
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

car_tracker = cv2.CascadeClassifier(car_classifier)

cars = car_tracker.detectMultiScale(gray_img,1.09,5)

print(cars)
for (x,y,a,b) in cars:
    cv2.rectangle(img, (x, y), (x+a, y+b), (0,255,0), 2)
    cv2.putText(img, 'Car', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0),2)

cv2.imshow('my detection', img)
cv2.waitKey()