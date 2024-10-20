import os
import cv2
import numpy as np

def remove_background_grabcut(input_image_path, output_image_path):
    """Remove background from image using GrabCut algorithm and make it transparent with feathering."""
    img = cv2.imread(input_image_path)
    h, w = img.shape[:2]
    
    # Create a mask initialized to the background
    mask = np.zeros((h, w), np.uint8)
    
    # Define the bounding box for the initial segmentation
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

    # Apply Gaussian blur to the mask for feathering effect
    mask2 = cv2.GaussianBlur(mask2.astype(np.float32), (21, 21), 0)
    mask2 = np.clip(mask2, 0, 1)  # Ensure values are between 0 and 1

    # Create an RGBA image with a transparent background
    img_result = img * mask2[:, :, np.newaxis]
    
    # Create an alpha channel
    alpha_channel = (mask2 * 255).astype(np.uint8)  # Scale to 255 for the alpha channel
    img_result = cv2.cvtColor(img_result, cv2.COLOR_BGR2BGRA)  # Convert to BGRA
    img_result[:, :, 3] = alpha_channel  # Set the alpha channel

    # Save the image with transparency
    cv2.imwrite(output_image_path, img_result)
    print(f"Background removed and saved as '{output_image_path}'")
    
    return img_result  # Return the image result for further processing

def upscale_image(img, output_image_path, scale_factor=8):
    """Upscale image by the given scale factor using bicubic interpolation and save as JPG."""
    # Convert to 8-bit unsigned integer if necessary
    if img.dtype != np.uint8:
        img = cv2.convertScaleAbs(img)

    # Get the original dimensions and resize
    h, w = img.shape[:2]
    upscaled_img = cv2.resize(img, (w * scale_factor, h * scale_factor), interpolation=cv2.INTER_CUBIC)

    # Denoising (optional) to improve quality
    if upscaled_img.shape[2] == 4:  # If the image has an alpha channel
        upscaled_img_rgb = upscaled_img[:, :, :3]  # Extract only the RGB channels for denoising
        upscaled_img_denoised = cv2.fastNlMeansDenoisingColored(upscaled_img_rgb, None, 10, 10, 7, 21)
        upscaled_img_denoised = cv2.merge((upscaled_img_denoised, upscaled_img[:, :, 3]))  # Merge alpha channel back
    else:
        upscaled_img_denoised = cv2.fastNlMeansDenoisingColored(upscaled_img, None, 10, 10, 7, 21)

    # Save as JPG with high quality
    cv2.imwrite(output_image_path, upscaled_img_denoised, [int(cv2.IMWRITE_JPEG_QUALITY), 95])  # 95 for high quality
    print(f"Upscaled image saved as '{output_image_path}'")

def process_images_in_folder(folder_path, output_folder_path):
    """Process all images in a folder to remove background and upscale."""
    os.makedirs(output_folder_path, exist_ok=True)  # Create output folder if it doesn't exist

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):  # Supported formats
            input_image_path = os.path.join(folder_path, filename)

            # Remove background and save as PNG
            png_output_path = os.path.join(output_folder_path, f"object_{filename.split('.')[0]}.png")
            img_result = remove_background_grabcut(input_image_path, png_output_path)

            # Upscale and save as JPG
            jpg_output_path = os.path.join(output_folder_path, f"upscaled_{filename.split('.')[0]}.jpg")
            upscale_image(img_result, jpg_output_path, scale_factor=8)  # Set scale factor to 8

if __name__ == "__main__":
    folder_path = r"C:\Users\Administrator\Desktop\ADOBE-STOCKS\IMAGE"  # Input folder path
    output_folder_path = r"C:\Users\Administrator\Desktop\ADOBE-STOCKS\IMAGE-PRO"  # Output folder path
    process_images_in_folder(folder_path, output_folder_path)
