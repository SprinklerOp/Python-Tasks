import cv2

def capture_frames(cam1, cam2):
    cap1 = cv2.VideoCapture(cam1)
    cap2 = cv2.VideoCapture(cam2)

    while True:
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        if not (ret1 and ret2):
            print("Failed to capture frames")
            break

        frame1 = cv2.resize(frame1, (640, 480))
        frame2 = cv2.resize(frame2, (640, 480))

        combined_frame = cv2.hconcat([frame1, frame2])
        cv2.imshow('Combined Frames', combined_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    camera1_index = 0
    camera2_index = 1

    capture_frames(camera1_index, camera2_index)
