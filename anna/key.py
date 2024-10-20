import csv
import os
import random

def read_file(file_path):
    """Reads a file and returns a list of lines."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

def generate_description(title):
    """Generates a unique description based on the title."""
    return f"This is a unique description for the title: '{title}'"

def list_images_from_folder(folder_path):
    """Lists all image files in a given folder."""
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
    return [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and os.path.splitext(f)[1].lower() in image_extensions]

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

def create_metadata_csv(titles, keywords, qualities, versions, images, output_file, category_number):
    """Creates a CSV file with Adobe Stock metadata structure."""
    fieldnames = ['Filename', 'Title', 'Keywords', 'Category', 'Release(s)']

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        num_keywords = len(keywords)

        for image in images:
            title = random.choice(titles)  # Randomly choose a title
            quality = random.choice(qualities)
            version = random.choice(versions)
            unique_title = f"{title}, {quality}, {version}"
            description = generate_description(unique_title)
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
    images_folder = r'C:\Users\Administrator\Desktop\ADOBE-STOCKS\IMAGE\OUTPUT'
    output_csv = 'FOR-UPLOAD-metadata.csv'

    # Expanded attributes (qualities and versions)
    qualities = [
        'HD', 'HDR', 'Ultra HD', 'High Definition', 
        'Super HD', 'Super Resolution'
    ]

    versions = [
        'Smooth Version', 'Smoother Version', 'Colored Light', 
        'Vibrant Colors', 'High Contrast', 'Soft Focus', 
        'Dynamic Range', 'Brightened', 'Enhanced Detail', 'Artistic Filter'
    ]

    # Read keywords and titles from files
    keywords = read_file(keywords_file)
    titles = read_file(titles_file)

    # List images from the IMAGE-PRO folder
    images = list_images_from_folder(images_folder)

    # Prompt for category selection
    category_number = get_category_choice()

    # Generate the metadata CSV for Adobe Stock with category selection
    create_metadata_csv(titles, keywords, qualities, versions, images, output_csv, category_number)
