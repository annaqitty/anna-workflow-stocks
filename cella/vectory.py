import cv2
import numpy as np
import zipfile
import os
from collections import Counter

def color_group(pixel):
    r, g, b = pixel[:3]

    # Dark Colors
    if r < 50 and g < 50 and b < 50:  # Black
        return "Dark Color: Black"
    elif r < 70 and g < 70 and b < 70:  # Dark Gray
        return "Dark Color: Dark Gray"
    elif r < 50 and g < 50 and b > 50:  # Dark Blue
        return "Dark Color: Dark Blue"
    elif r < 50 and g > 50 and b < 50:  # Dark Red
        return "Dark Color: Dark Red"
    elif r < 50 and g > 50 and b > 50:  # Dark Cyan
        return "Dark Color: Dark Cyan"
    elif r < 100 and g < 100 and b > 100:  # Dark Magenta
        return "Dark Color: Dark Magenta"
    elif r < 100 and g > 100 and b < 100:  # Dark Green
        return "Dark Color: Dark Green"
    
    # Soft Colors
    elif r > 150 and g > 100 and b > 100:  # Soft Pink
        return "Soft Color: Soft Pink"
    elif r > 200 and g > 200 and b < 150:  # Soft Yellow
        return "Soft Color: Soft Yellow"
    elif r < 200 and g > 150 and b < 200:  # Soft Purple
        return "Soft Color: Soft Purple"
    elif r < 200 and g < 200 and b > 150:  # Soft Blue
        return "Soft Color: Soft Blue"
    elif r > 100 and g < 100 and b > 100:  # Soft Magenta
        return "Soft Color: Soft Magenta"
    elif r < 150 and g < 150 and b > 150:  # Soft Light Gray
        return "Soft Color: Soft Light Gray"
    
    # Light Colors
    elif r > 200 and g > 200 and b < 100:  # Light Yellow
        return "Light Color: Light Yellow"
    elif r > 200 and g < 200 and b > 200:  # Light Magenta
        return "Light Color: Light Magenta"
    elif r < 150 and g > 200 and b < 150:  # Light Green
        return "Light Color: Light Green"
    elif r < 150 and g < 150 and b > 200:  # Light Blue
        return "Light Color: Light Blue"
    elif r > 200 and g < 150 and b < 150:  # Light Red
        return "Light Color: Light Red"
    elif r < 200 and g > 200 and b > 200:  # Light Gray
        return "Light Color: Light Gray"
    elif r > 150 and g > 50 and b < 50:  # Light Coral
        return "Light Color: Light Coral"
    elif r < 200 and g > 200 and b > 100:  # Light Olive
        return "Light Color: Light Olive"

    return "Other"

def dominant_colors(bitmap, num_colors=5):
    pixels = bitmap.reshape(-1, 3)
    counter = Counter(map(tuple, pixels))
    return [color for color, _ in counter.most_common(num_colors)]

def create_gradient_svg(dominant_colors):
    if not dominant_colors:
        return '<rect width="100%" height="100%" fill="white"/>\n'  # Fallback to white background

    gradient_id = "bgGradient"
    stops = ""
    for i, color in enumerate(dominant_colors):
        r, g, b = color
        stop_pos = int((i / (len(dominant_colors) - 1)) * 100)
        stops += f'<stop offset="{stop_pos}%" stop-color="rgb({r},{g},{b})"/>\n'
    
    return f'<defs><linearGradient id="{gradient_id}" x1="0%" y1="0%" x2="100%" y2="0%">{stops}</linearGradient></defs>\n<rect width="100%" height="100%" fill="url(#{gradient_id})"/>\n'

def convert_png_to_vector(input_png, output_svg, canvas_size=(1920, 1080)):
    # Load the image
    image = cv2.imread(input_png)
    if image is None:
        raise ValueError(f"Could not read the image: {input_png}")

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Create a blank canvas with specified size
    canvas_height, canvas_width = canvas_size
    canvas = np.ones((canvas_height, canvas_width, 3), dtype=np.uint8) * 255  # White background

    # Resize and center the image on the canvas
    new_width = int(canvas_width * 0.75)
    new_height = int(canvas_height * 0.75)
    resized_image = cv2.resize(image_rgb, (new_width, new_height))

    y_offset = (canvas_height - new_height) // 2
    x_offset = (canvas_width - new_width) // 2
    canvas[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = resized_image

    # Get dominant colors
    dominant_colors_list = dominant_colors(canvas)

    # Create SVG output
    with open(output_svg, 'w') as svg_file:
        svg_file.write('<svg xmlns="http://www.w3.org/2000/svg" version="1.1">\n')
        
        # Add gradient background
        gradient_svg = create_gradient_svg(dominant_colors_list)
        svg_file.write(gradient_svg)

        # Create color groups
        color_groups = {
            "Dark Color": [],
            "Soft Color": [],
            "Light Color": [],
            "Other": []
        }

        # Iterate through pixels to group by color
        for y in range(canvas.shape[0]):
            for x in range(canvas.shape[1]):
                color_name = color_group(canvas[y, x])
                color_group_name = color_name.split(":")[0]
                color_groups[color_group_name].append((x, y))

        # Write background rectangle with gradient
        svg_file.write('<g id="Background">\n')
        svg_file.write('<rect width="100%" height="100%" fill="url(#bgGradient)"/>\n')
        svg_file.write('</g>\n')

        # Write color groups to SVG
        for group, pixels in color_groups.items():
            if pixels:
                svg_file.write(f'<g id="{group}">\n')
                for pixel in pixels:
                    svg_file.write(f'<rect x="{pixel[0]}" y="{pixel[1]}" width="1" height="1" fill="{group}"/>\n')
                svg_file.write('</g>\n')

        svg_file.write('</svg>\n')

def create_zip(input_png, output_svg, zip_filename):
    with zipfile.ZipFile(zip_filename, 'w') as zf:
        zf.write(input_png, os.path.basename(input_png))
        zf.write(output_svg, os.path.basename(output_svg))
        zf.writestr('output_image.ai', 'This is a placeholder for the AI file.\nConvert SVG to AI using Illustrator.')

def process_images_in_folder(input_folder, canvas_size=(1920, 1080)):
    for filename in os.listdir(input_folder):
        if filename.endswith('.png'):
            input_png = os.path.join(input_folder, filename)
            output_svg = os.path.splitext(input_png)[0] + '.svg'
            zip_filename = os.path.splitext(input_png)[0] + '.zip'
            
            convert_png_to_vector(input_png, output_svg, canvas_size)
            create_zip(input_png, output_svg, zip_filename)
            
            print(f"Processed {input_png}: Created {output_svg} and {zip_filename}")

# Usage
input_folder = 'IMAGE-PRO'  # Change this to your input folder path
canvas_size = (1920, 1080)  # Full HD canvas size
process_images_in_folder(input_folder, canvas_size)
