from PIL import Image, ImageDraw, ImageFont
import random

def create_chatbot_background(width, height, num_doodles):
    # Create a blank image with a greyish background
    background_color = (220, 220, 220)
    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # Define colors for doodles
    doodle_colors = [(128, 128, 128), (169, 169, 169), (192, 192, 192)]

    # Draw random doodles (planets and satellites)
    for _ in range(num_doodles):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(10, 50)
        color = random.choice(doodle_colors)

        draw.ellipse([x, y, x + size, y + size], fill=color)

    return image

# Adjust the width, height, and num_doodles as needed
width = 800
height = 600
num_doodles = 50

# Generate the background image
background_image = create_chatbot_background(width, height, num_doodles)

# Save or display the image
background_image.save("chatbot_background.png")
background_image.show()