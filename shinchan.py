from PIL import Image, ImageDraw, ImageFont

# Create a new image with a blue background
width, height = 500, 500
image = Image.new("RGB", (width, height), "blue")

# Create a drawing object
draw = ImageDraw.Draw(image)

# Draw the character (Shinchan) - This will be a simple representation

# Face
face_color = (255, 204, 153)
draw.ellipse((200, 100, 300, 200), fill=face_color, outline="black")

# Eyes
eye_color = "white"
eye_outline = "black"
draw.ellipse((225, 130, 250, 155), fill=eye_color, outline=eye_outline)
draw.ellipse((250, 130, 275, 155), fill=eye_color, outline=eye_outline)

# Pupils
pupil_color = "black"
draw.ellipse((235, 140, 240, 145), fill=pupil_color)
draw.ellipse((260, 140, 265, 145), fill=pupil_color)

# Mouth
draw.ellipse((240, 160, 260, 180), fill="red", outline="black")

# Body
body_color = (255, 0, 0)
draw.rectangle((200, 200, 300, 300), fill=body_color, outline="black")

# Shorts
shorts_color = (255, 255, 102)
draw.rectangle((200, 300, 300, 350), fill=shorts_color, outline="black")

# Legs
leg_color = face_color
draw.rectangle((220, 350, 240, 400), fill=leg_color, outline="black")
draw.rectangle((260, 350, 280, 400), fill=leg_color, outline="black")

# Feet
feet_color = (255, 204, 153)
draw.rectangle((220, 400, 240, 410), fill=feet_color, outline="black")
draw.rectangle((260, 400, 280, 410), fill=feet_color, outline="black")

# Arms
draw.rectangle((175, 225, 200, 245), fill=face_color, outline="black")  # Left arm
draw.rectangle((300, 225, 325, 245), fill=face_color, outline="black")  # Right arm

# Peace sign fingers (Left hand)
draw.rectangle((165, 210, 175, 225), fill=face_color, outline="black")  # Finger 1
draw.rectangle((155, 215, 165, 225), fill=face_color, outline="black")  # Finger 2

# Peace sign fingers (Right hand)
draw.rectangle((325, 210, 335, 225), fill=face_color, outline="black")  # Finger 1
draw.rectangle((335, 215, 345, 225), fill=face_color, outline="black")  # Finger 2

# Save the image
image.save("shinchan.png")

# Display the image
image.show()
