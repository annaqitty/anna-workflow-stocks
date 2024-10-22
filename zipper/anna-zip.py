import os
import zipfile
from collections import defaultdict

def create_zip_from_same_name_files(folder_path):
    # Dictionary to store base names and their corresponding files
    file_dict = defaultdict(list)

    # Iterate through all files in the specified folder
    for filename in os.listdir(folder_path):
        # Split the file name and extension
        base_name, ext = os.path.splitext(filename)
        ext = ext.lower()  # Normalize the extension to lowercase
        file_dict[base_name].append(filename)  # Store full filename

    # Create a zip file for each base name with different extensions
    for base_name, files in file_dict.items():
        if len(set(os.path.splitext(f)[1] for f in files)) > 1:  # Check for different extensions
            zip_file_name = os.path.join(folder_path, f"{base_name}.zip")
            with zipfile.ZipFile(zip_file_name, 'w') as zip_file:
                for file in files:
                    zip_file.write(os.path.join(folder_path, file), arcname=file)
            print(f"Created zip file: {zip_file_name}")

# Example usage
folder_path = r"C:\Users\Administrator\Desktop\ADOBE-STOCKS\IMAGE\OUTPUT"  # Change this to your folder path
create_zip_from_same_name_files(folder_path)
