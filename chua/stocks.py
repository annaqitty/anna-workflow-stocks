import os
import time
import cv2
import numpy as np
import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init(autoreset=True)

def remove_background_grabcut(input_image_path):
    """Remove background from image using GrabCut algorithm and make it transparent with feathering."""
    img = cv2.imread(input_image_path)
    h, w = img.shape[:2]

    mask = np.zeros((h, w), np.uint8)
    rectangle = (1, 1, w - 1, h - 1)

    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)

    mask[1:h-1, 1:w-1] = cv2.GC_PR_FGD
    cv2.grabCut(img, mask, rectangle, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_MASK)

    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    mask2 = cv2.GaussianBlur(mask2.astype(np.float32), (21, 21), 0)
    mask2 = np.clip(mask2, 0, 1)

    img_result = img * mask2[:, :, np.newaxis]
    alpha_channel = (mask2 * 255).astype(np.uint8)
    img_result = cv2.cvtColor(img_result, cv2.COLOR_BGR2BGRA)
    img_result[:, :, 3] = alpha_channel

    return img_result

def upscale_image_with_dnn(img):
    """Upscale image using DNN-based super resolution (4x)."""
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    model_path = "EDSR_x4.pb"  # Ensure you have the model
    sr.readModel(model_path)
    sr.setModel("edsr", 4)

    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)  # Convert to BGR if it has an alpha channel
    return sr.upsample(img)

def process_image(input_image_path, output_folder_path):
    """Process a single image: remove background and upscale."""
    png_output_path = os.path.join(output_folder_path, f"{os.path.basename(input_image_path).split('.')[0]}.png")
    
    img_result = remove_background_grabcut(input_image_path)
    jpg_output_path = os.path.join(output_folder_path, f"{os.path.basename(input_image_path).split('.')[0]}.jpg")
    
    upscaled_img = upscale_image_with_dnn(img_result)

    # Save outputs
    cv2.imwrite(png_output_path, img_result)
    cv2.imwrite(jpg_output_path, upscaled_img)

    return os.path.basename(input_image_path)

def process_images_in_folder(folder_path, output_folder_path):
    """Process all images in a folder to remove background and upscale."""
    os.makedirs(output_folder_path, exist_ok=True)
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]

    start_time = time.time()
    total_files = len(files)
    for idx, filename in enumerate(files):
        input_image_path = os.path.join(folder_path, filename)
        print(f"Processing {filename}... ", end='', flush=True)

        try:
            process_image(input_image_path, output_folder_path)
            print(Fore.GREEN + f"Processed {filename}")
        except Exception as e:
            print(Fore.RED + f"Error processing {filename}: {e}")

        # Estimate remaining time
        elapsed_time = time.time() - start_time
        estimated_time = (elapsed_time / (idx + 1)) * (total_files - (idx + 1))
        print(f"Estimated time remaining: {estimated_time:.2f} seconds.")

    total_time = time.time() - start_time
    print(f"All files processed successfully in {total_time:.2f} seconds.")

if __name__ == "__main__":
    folder_path = r"C:\Users\Administrator\Desktop\ADOBE-STOCKS\IMAGE"
    output_folder_path = r"C:\Users\Administrator\Desktop\ADOBE-STOCKS\IMAGE-PRO"
    process_images_in_folder(folder_path, output_folder_path)
