import os
import cv2
from PIL import Image


# Define a mapping for color names to RGB values
color_mapping = {
    "red": (255, 0, 0),
    "purple": (128, 0, 128),
    "orange": (255, 165, 0),
    "green": (0, 128, 50),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0)
}

# Reload the image to start fresh
image = Image.open(name_image_2work)
draw = ImageDraw.Draw(image)

# Define a font size for the labels using the default PIL font
font_size = 100
#font = ImageFont.load_default()

font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/Ubuntu-M.ttf", 30, encoding="unic")

# Update the draw_box function to use the larger font size with the default font
def draw_box(row):
    x0, y0, x1, y1 = row['x0'], row['y0'], row['x1'], row['y1']
    color = color_mapping.get(row['color'], (0, 0, 0)) # Default to black if color not found
    draw.rectangle([x0, y0, x1, y1], outline=color, width=3)
    label = str(row['label']) if pd.notnull(row['label']) else None # Check for missing label
    if label:
        draw.text((x0 + 5, y0 + 5), label, fill=color, font=font)

# Draw the boundaries
#draw_box(boundaries_info)


def draw_box_model(modelo,
                   boundaries_info=None,
                   sections_info=None,
                   frames_info=None,
                   field_boxes_info=None,
                   draw_boundaries=True,
                   draw_sections=True,
                   draw_frames=True,
                   draw_field_boxes=True):
    
    # Draw boundaries if requested
    if draw_boundaries and boundaries_info is not None:
        filtered_boundaries_info = boundaries_info[boundaries_info['model'] == modelo]
        for index, row in filtered_boundaries_info.iterrows():
            draw_box(row)

    # Draw sections if requested
    if draw_sections and sections_info is not None:
        filtered_sections_info = sections_info[sections_info['model'] == modelo]
        for index, row in filtered_sections_info.iterrows():
            draw_box(row)
            
    # Draw frames if requested
    if draw_frames and frames_info is not None:
        filtered_frames_info = frames_info[frames_info['model'] == modelo]
        for index, row in filtered_frames_info.iterrows():
            draw_box(row)
            
    # Draw field boxes if requested
    if draw_field_boxes and field_boxes_info is not None:
        filtered_field_boxes_info = field_boxes_info[field_boxes_info['model'] == modelo]
        for index, row in filtered_field_boxes_info.iterrows():
            draw_box(row)
    
    # Show the image with selected drawings
    image.show()