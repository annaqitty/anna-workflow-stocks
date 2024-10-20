import csv
import os
import random
import shutil

def rename_images(input_folder, output_folder):
    """Rename all image files in the specified folder and copy them to the output folder."""
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
    
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Get list of files in the input folder
    files = os.listdir(input_folder)
    
    # Filter out only image files
    image_files = [f for f in files if os.path.isfile(os.path.join(input_folder, f)) and os.path.splitext(f)[1].lower() in image_extensions]
    
    renamed_files = []
    
    # Rename and copy each image file
    for i, filename in enumerate(image_files):
        # Get file extension
        file_ext = os.path.splitext(filename)[1]
        
        # Form new file name (IMG_202403_1, IMG_202403_2, ...)
        new_filename = f"IMAGE_2024070808_0075205{i+1}{file_ext}"
        
        # Construct full paths
        current_path = os.path.join(input_folder, filename)
        new_path = os.path.join(output_folder, new_filename)
        
        # Copy and rename file
        try:
            shutil.copy(current_path, new_path)
            print(f"Renamed and copied '{filename}' to '{new_filename}'")
            renamed_files.append(new_filename)  # Store renamed files
        except Exception as e:
            print(f"Failed to copy '{filename}': {str(e)}")

    return renamed_files

def read_file(file_path):
    """Reads a file and returns a list of lines."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

def get_category_choice():
    """Prompt user for category number and validate."""
    while True:
        try:
            category_number = int(input("Enter the number corresponding to the category:\n"
                                        "1. Animals\n"
                                        "2. Buildings and Architecture\n"
                                        "3. Business\n"
                                        "4. Drinks\n"
                                        "5. The Environment\n"
                                        "6. States of Mind\n"
                                        "7. Food\n"
                                        "8. Graphic Resources\n"
                                        "9. Hobbies and Leisure\n"
                                        "10. Industry\n"
                                        "11. Landscapes\n"
                                        "12. Lifestyle\n"
                                        "13. People\n"
                                        "14. Plants and Flowers\n"
                                        "15. Culture and Religion\n"
                                        "16. Science\n"
                                        "17. Social Issues\n"
                                        "18. Sports\n"
                                        "19. Technology\n"
                                        "20. Transport\n"
                                        "21. Travel\n"
                                        "Enter your choice: "))
            if 1 <= category_number <= 21:
                return category_number
            else:
                print("Invalid category number. Please enter a number between 1 and 21.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def create_metadata_csv(titles, keywords, images, output_file, category_number):
    """Creates a CSV file with Adobe Stock metadata structure."""
    fieldnames = ['Filename', 'Title', 'Keywords', 'Category', 'Release(s)']

    # Commonly used qualities and versions
    qualities = [
        'High Quality', 'Ultra HD', 'Premium Quality', 'Customed Quality', 
        'High Resolution'
    ]

    versions = [
        'Standard Version', 'Enhanced Version', 'Professional Version', 
        'Extended Version', 'Basic Version', 'Slightly Edited Version',
        'Creative Version', 'Exclusive Version'
    ]

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for image in images:
            title = random.choice(titles)  # Randomly choose a title
            quality = random.choice(qualities)  # Randomly choose a quality
            version = random.choice(versions)  # Randomly choose a version
            unique_title = f"{title}, {quality}, {version}"
            keyword = ', '.join(random.choice(keywords) for _ in range(random.randint(3, 6)))  # Randomly select 3-6 keywords

            # Use the provided category number
            category = category_number

            # Use the final title as the release name
            release = unique_title

            writer.writerow({
                'Filename': image,
                'Title': unique_title,
                'Keywords': keyword,
                'Category': category,
                'Release(s)': release
            })

    print(f"Metadata CSV '{output_file}' created successfully for {len(images)} images.")

if __name__ == "__main__":
    # File paths and configurations
    keywords_file = 'keyword.txt'
    titles_file = 'tittle-roll.txt'
    input_folder = 'IMAGE'      # Input folder for images
    output_folder = 'IMAGE-PRO'  # Output folder for renamed images
    output_csv = os.path.join(output_folder, 'police-metadata.csv')

    # Read keywords and titles from files
    keywords = read_file(keywords_file)
    titles = read_file(titles_file)

    # Rename images and get the list of renamed images
    renamed_images = rename_images(input_folder, output_folder)

    # Prompt for category selection
    category_number = get_category_choice()

    # Generate the metadata CSV for Adobe Stock with category selection
    create_metadata_csv(titles, keywords, renamed_images, output_csv, category_number)
