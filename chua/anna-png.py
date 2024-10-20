import os
import cv2
import numpy as np

def remove_background_grabcut(input_image_path, output_image_path):
    """Remove background from image using GrabCut algorithm and make it transparent with feathering."""
    img = cv2.imread(input_image_path)
    h, w = img.shape[:2]
    
    # Create a mask initialized to the background
    mask = np.zeros((h, w), np.uint8)
    
    # Define the bounding box
    rectangle = (1, 1, w - 1, h - 1)

    # Create background and foreground models
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)

    # Initialize the mask for GrabCut
    mask[1:h-1, 1:w-1] = cv2.GC_PR_FGD  # Assume that the inside of the rectangle is foreground

    # Apply GrabCut
    cv2.grabCut(img, mask, rectangle, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_MASK)

    # Create a binary mask where 1 indicates the foreground
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

    # Apply Gaussian blur to the mask for feathering
    mask2 = cv2.GaussianBlur(mask2.astype(np.float32), (21, 21), 0)
    mask2 = np.clip(mask2, 0, 1)  # Ensure values are between 0 and 1

    # Create an RGBA image with a transparent background
    img_result = img * mask2[:, :, np.newaxis]
    
    # Create an alpha channel (scaled for the alpha channel)
    alpha_channel = (mask2 * 255).astype(np.uint8)  # Scale to 255 for the alpha channel
    img_result = cv2.cvtColor(img_result, cv2.COLOR_BGR2BGRA)  # Convert to BGRA
    img_result[:, :, 3] = alpha_channel  # Set the alpha channel

    # Save the image with transparency
    cv2.imwrite(output_image_path, img_result)
    print(f"Background removed and saved as '{output_image_path}'")

def process_images_in_folder(folder_path):
    """Process all images in a folder to remove background."""
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):  # Add more formats as needed
            input_image_path = os.path.join(folder_path, filename)
            output_image_path = os.path.join(folder_path, f"modified_{filename.split('.')[0]}.png")  # Save as PNG

            remove_background_grabcut(input_image_path, output_image_path)

if __name__ == "__main__":
    folder_path = r"C:\Users\Administrator\Desktop\ADOBE-STOCKS\DL"  # Update with your folder path
    process_images_in_folder(folder_path)
