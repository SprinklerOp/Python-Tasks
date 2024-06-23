import cv2

datta = cv2.VideoCapture(0)
status_usb, photo_usb = datta.read()

if status_usb:
    cv2.imwrite("datta.png", photo_usb)
    cv2.imshow("USB Camera", photo_usb)
else:
    print("Error: Could not read from USB camera.")

camera_url = "http://192.0.0.4:8080/video"  
datta_phone = cv2.VideoCapture(camera_url)
status_ip, photo_ip = datta_phone.read()

if status_ip:
    cv2.imwrite("camera_photo.png", photo_ip)
    cv2.imshow("IP Camera", photo_ip)
else:
    print("Error: Could not read from IP camera.")

cv2.waitKey(5000)

cv2.destroyAllWindows()

datta.release()
datta_phone.release()

