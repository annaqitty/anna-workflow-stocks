import os

def rename_images(folder_path):
    """Rename all image files in the specified folder."""
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
    
    # Get list of files in the folder
    files = os.listdir(folder_path)
    
    # Filter out only image files
    image_files = [f for f in files if os.path.isfile(os.path.join(folder_path, f)) and os.path.splitext(f)[1].lower() in image_extensions]
    
    # Rename each image file
    for i, filename in enumerate(image_files):
        # Get file extension
        file_ext = os.path.splitext(filename)[1]
        
        # Form new file name (IMG_202403_1, IMG_202403_2, ...)
        new_filename = f"IMG_2024070002_0781815{i+1}{file_ext}"
        
        # Construct full paths
        current_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_filename)
        
        # Rename file
        try:
            os.rename(current_path, new_path)
            print(f"Renamed '{filename}' to '{new_filename}'")
        except Exception as e:
            print(f"Failed to rename '{filename}': {str(e)}")

if __name__ == "__main__":
    # Specify the folder path containing images
    folder_path = r'C:\Users\Administrator\Desktop\ADOBE-STOCKS\IMAGE\OUTPUT'
    
    # Call the function to rename images
    rename_images(folder_path)
