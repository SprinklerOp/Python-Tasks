import cv2
a=cv2.VideoCapture(0)
status,photo=a.read()
status
cv2.imwrite("datta.png",photo)
cv2.imshow("datta.png",photo)
cv2.waitKey(5000)
cv2.destroyAllWindows()