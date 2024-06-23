import numpy as np
import matplotlib.pyplot as plt


height = 300
width = 300

cartoon_image = np.zeros((height, width, 3), dtype=np.uint8)


white = [255, 255, 255]
black = [0, 0, 0]
blue = [0, 0, 255]
red = [255, 0, 0]
yellow = [255, 255, 0]


cartoon_image[:] = white


face_center = (150, 150)
face_radius = 100
y, x = np.ogrid[:height, :width]
mask = (x - face_center[0])**2 + (y - face_center[1])**2 <= face_radius**2
cartoon_image[mask] = yellow


eye_radius = 15
left_eye_center = (110, 120)
right_eye_center = (190, 120)
mask_left_eye = (x - left_eye_center[0])**2 + (y - left_eye_center[1])**2 <= eye_radius**2
mask_right_eye
