import cv2

def detect_faces(image):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
    return faces

def display_live_video():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        faces = detect_faces(frame)
        display_frame = frame.copy()

        if len(faces) > 0:
            x_face, y_face, w_face, h_face = faces[0]
            face_crop = frame[y_face:y_face+h_face, x_face:x_face+w_face]
            display_frame[y_face:y_face+h_face, x_face:x_face+w_face] = face_crop

        cv2.imshow("Live Video", display_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    display_live_video()
