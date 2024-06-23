import cv2
import mediapipe
from cvzone.HandTrackingModule import HandDetector
cap = cv2.VideoCapture(0)
status, photo= cap.read()
cv2.imshow("datta",photo)
cv2.waitKey()
cv2.destroyAllWindows()
cap = cv2.VideoCapture(0)
status, photo= cap.read()
cv2.imshow("datta",photo)
cv2.waitKey()
cv2.destroyAllWindows()
detect= HandDetector()
detect.findHands(photo)
