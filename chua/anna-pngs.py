import os
import cv2
import numpy as np
import pandas as pd
import requests
import tensorflow as tf

# Load a pre-trained model for image analysis (e.g., MobileNetV2)
model = tf.keras.applications.MobileNetV2(weights='imagenet')

def remove_background_grabcut(input_image_path, output_image_path):
    """Remove background from image using GrabCut algorithm and make it transparent."""
    img = cv2.imread(input_image_path)
    if img is None:
        print(f"Error: Could not read image '{input_image_path}'.")
        return

    h, w = img.shape[:2]
    
    # Create a mask initialized to the background
    mask = np.zeros((h, w), np.uint8)
    rectangle = (1, 1, w - 1, h - 1)

    # Background and foreground models
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)

    # Initialize the mask
    mask[1:h-1, 1:w-1] = cv2.GC_PR_FGD

    # Apply GrabCut
    cv2.grabCut(img, mask, rectangle, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_MASK)

    # Create binary mask
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

    # Apply Gaussian blur
    mask2 = cv2.GaussianBlur(mask2.astype(np.float32), (21, 21), 0)
    mask2 = np.clip(mask2, 0, 1)

    # Create an RGBA image
    img_result = img * mask2[:, :, np.newaxis]
    alpha_channel = (mask2 * 255).astype(np.uint8)
    img_result = cv2.cvtColor(img_result, cv2.COLOR_BGR2BGRA)
    img_result[:, :, 3] = alpha_channel

    # Save the image
    cv2.imwrite(output_image_path, img_result)
    print(f"Background removed and saved as '{output_image_path}'")

def analyze_image(image_path):
    """Analyze the image to generate keywords and title based on content."""
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))  # Resize for MobileNetV2
    img = tf.keras.applications.mobilenet_v2.preprocess_input(img)
    img = np.expand_dims(img, axis=0)

    predictions = model.predict(img)
    decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=5)[0]
    
    keywords = ", ".join([pred[1] for pred in decoded_predictions])
    title = f"Image of {decoded_predictions[0][1]}"

    return title, keywords

def generate_ai_metadata(image_filename, api_key):
    """Generate additional metadata using AI (Gemini)."""
    api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
    
    prompt = f"Generate a catchy title, 40 relevant keywords for stock image sales, a suitable category, and release information for the image: '{image_filename}'."
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    
    headers = {
        "Content-Type": "application/json",
    }
    
    response = requests.post(f"{api_url}?key={api_key}", json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching metadata: {response.status_code}, {response.text}")
        return None

def process_images_in_folder(folder_path, output_folder_path, api_key):
    """Process all images in a folder to remove background and generate metadata."""
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    metadata_list = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            input_image_path = os.path.join(folder_path, filename)
            output_image_path = os.path.join(output_folder_path, f"modified_{filename.split('.')[0]}.png")

            remove_background_grabcut(input_image_path, output_image_path)

            # Analyze the image for keywords and title
            title, keywords = analyze_image(input_image_path)

            # Generate additional metadata
            ai_metadata = generate_ai_metadata(filename, api_key)

            if ai_metadata:
                category = ai_metadata.get('category', "General")
                release_info = ai_metadata.get('release', "No Release Info")
            else:
                category = "General"
                release_info = "No Release Info"

            # Prepare the metadata entry
            metadata_entry = {
                'Filename': output_image_path,
                'Title': title,
                'Keywords': keywords,
                'Category': category,
                'Release(s)': release_info
            }
            metadata_list.append(metadata_entry)

    # Save the metadata to CSV
    if metadata_list:
        metadata_df = pd.DataFrame(metadata_list)
        csv_file_path = os.path.join(output_folder_path, "metadata.csv")
        metadata_df.to_csv(csv_file_path, index=False)
        print(f"Metadata saved as '{csv_file_path}'")

if __name__ == "__main__":
    input_folder_path = r"C:\Users\Administrator\Desktop\ADOBE-STOCKS\IMAGE"  # Update with your input folder path
    output_folder_path = r"C:\Users\Administrator\Desktop\ADOBE-STOCKS\IMAGE"  # Custom output folder path
    api_key = "AIzaSyDqk4X3R2JmZ40FuPZqlvR5GSAxB1GlSe4"  # Replace with your actual API key
    process_images_in_folder(input_folder_path, output_folder_path, api_key)
